"""
Custom RAG agent based on Langchain and OCI GenAI
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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
QA_SYSTEM_PROMPT = """You are an AI assistant for question-answering tasks. \
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

    Usage:

    """

    # TODO: add the management of the session
    # storing, for each session, the chat history
    def __init__(self, should_stream: bool = False):
        """
        Initialize the client
        """
        self.config = ConfigReader("config.toml")

        self.top_k = self.config.find_key("custom_rag_top_k")
        # the name of the DB table
        self.collection_name = self.config.find_key("collection_name")
        self.should_stream = should_stream
        self.logger = get_console_logger()

    def create_session(self):
        """
        Create a session with the agent
        """
        return

    def chat(self, session_id: str, message: str):
        """
        Chat with the agent
        """
        # actually don't create, get a reference to the vector store
        v_store = create_vector_store(self.collection_name)

        llm = create_model_for_custom_rag()

        retriever = v_store.as_retriever(k=self.top_k)

        # create the RAG chain using Langchain
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, CONTEXT_Q_PROMPT
        )

        question_answer_chain = create_stuff_documents_chain(llm, QA_PROMPT)

        rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        # invoke llm
        # TODO: add the chat history
        ai_msg = rag_chain.invoke({"input": message, "chat_history": []})

        return ai_msg

    def close_session(self, session_id: str):
        """
        Close the session cancelling the chat history
        """
        return
