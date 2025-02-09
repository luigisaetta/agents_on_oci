"""
Custom RAG agent based on Langchain and OCI GenAI
"""

import uuid
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from oci_vector_store import create_vector_store
from oci_models import create_model_for_custom_rag
from config_reader import ConfigReader
from utils import get_console_logger

CONTEXT_Q_SYSTEM_PROMPT = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

CONTEXT_Q_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", CONTEXT_Q_SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

#
# The prompt for the answer from the LLM
#
QA_SYSTEM_PROMPT = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \

{context}"""

QA_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", QA_SYSTEM_PROMPT),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)


class OCICustomRAGagent:
    """
    This class provide an implementation of a custom RAG agent
    based on Langchain and OCI GenAI

    it also manage the chat history for each session
    Usage:

    """

    def __init__(self, should_stream: bool = False):
        """
        Initialize the client
        """
        self.config = ConfigReader("config.toml")

        self.top_k = self.config.find_key("custom_rag_top_k")
        # the name of the DB table
        self.collection_name = self.config.find_key("collection_name")
        self.should_stream = should_stream

        # dict to handle all the sessions
        self.sessions = {}
        self.logger = get_console_logger()

    def create_session(self):
        """
        Create a session with the agent
        """
        # create a unique session id
        session_id = str(uuid.uuid4())
        # init session history
        self.sessions[session_id] = []

        self.logger.info("Session %s created.", session_id)

        return session_id

    def _create_rag_chain(self):
        """
        Create the chain
        """
        # actually don't create, get a reference to the vector store
        v_store = create_vector_store(self.collection_name)

        llm = create_model_for_custom_rag()

        retriever = v_store.as_retriever(search_kwargs={"k": self.top_k})

        # create the RAG chain using Langchain
        # the chain is created to handle msg history
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, CONTEXT_Q_PROMPT
        )

        question_answer_chain = create_stuff_documents_chain(llm, QA_PROMPT)

        _rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )
        return _rag_chain

    def chat(self, session_id: str, message: str):
        """
        Chat with the agent
        """
        # get the chat history of the session
        chat_history = self.sessions[session_id]

        rag_chain = self._create_rag_chain()

        # invoke llm
        chain_output = rag_chain.invoke(
            {"input": message, "chat_history": chat_history}
        )

        # Update chat history with HumanMessage and AIMessage
        # be careful, since it is a chain, chain_output is not an AIMSg but a dict
        chat_history.append(HumanMessage(content=message))
        chat_history.append(AIMessage(content=chain_output["answer"]))

        return chain_output

    def close_session(self, session_id: str):
        """
        Close the session cancelling the chat history
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            self.logger.info("Session %s closed.", session_id)
        else:
            self.logger.warning("Session %s does not exist.", session_id)
