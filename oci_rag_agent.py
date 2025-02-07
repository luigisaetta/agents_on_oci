"""
This module wraps the code to call the OCI AI Agent
"""

import oci
from oci.generative_ai_agent_runtime import GenerativeAiAgentRuntimeClient
from oci.generative_ai_agent_runtime.models import CreateSessionDetails
from oci.generative_ai_agent_runtime.models import ChatDetails
from utils import get_console_logger


class OCIRAGAgent:
    """
    This class provide a client for OCI RAG agent

    Usage:
        you need to provide: agent_id and endpoint

    Limitations:
        for now, no support for citations in this client.
        It will be added soon
    """

    def __init__(self, agent_id: str, endpoint: str, should_stream: bool = False):
        """
        initialize the client

        :param agent_id: OCI agent id
        :param endpoint: OCI endpoint
        :param should_stream: if the response should be streamed
        """
        self.logger = get_console_logger()
        self.agent_id = agent_id
        self.endpoint = endpoint
        self.should_stream = should_stream

        # assuming API_KEY
        self.config = oci.config.from_file()

        # create the client
        self.client = GenerativeAiAgentRuntimeClient(
            self.config, service_endpoint=endpoint
        )

    def create_session(self):
        """
        Create a session with the agent
        """
        session_response = self.client.create_session(
            create_session_details=CreateSessionDetails(
                display_name="USER_Session", description="User Session"
            ),
            agent_endpoint_id=self.agent_id,
        )

        sess_id = session_response.data.id

        self.logger.info("Session created, ID: %s", sess_id)
        self.logger.info("")

        return sess_id

    def chat(self, session_id: str, message: str):
        """
        Chat with the agent
        """
        response = self.client.chat(
            agent_endpoint_id=self.agent_id,
            chat_details=ChatDetails(
                # to use the message history pass the same sess_id
                user_message=message,
                session_id=session_id,
                should_stream=self.should_stream,
            ),
        )

        if not self.should_stream:
            return response.data.message.content.text

        # streaming: should return a generator
        return response

    def close_session(self, session_id: str):
        """
        Close the session
        """
        self.client.delete_session(self.agent_id, session_id)

        self.logger.info("Session closed, ID: %s", session_id)
        self.logger.info("")
