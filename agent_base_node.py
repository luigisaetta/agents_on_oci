"""
Generic class for adding APM tracing.

This class is a base class for all nodes in the agent
"""

from abc import ABC, abstractmethod
from langchain_core.runnables import Runnable
from langchain_community.chat_models import ChatOCIGenAI

# added to integrate with APM
from py_zipkin import Encoding
from py_zipkin.zipkin import zipkin_span

from utils import get_console_logger
from config_private import COMPARTMENT_OCID

logger = get_console_logger()


class BaseAgentNode(Runnable, ABC):
    """
    This class is a base class for all nodes in the agent
    where you equip the node with APM tracing capabilities.
    It provides a common interface for running a node and a hook for adding
    custom logic
    """

    def __init__(self, service_name=None, json_schema=None):
        """
        Init the node with service name and json schema

        service_name (str): The name of the service, for tracing purposes.
        json_schema (dict): The JSON schema for input and output data.
        """
        self.service_name = service_name or "default_service"
        self.json_schema = json_schema

    def get_llm_model(
        self,
        model_id="meta.llama-3.3-70b-instruct",
        endpoint="https://inference.generativeai.eu-frankfurt-1.oci.oraclecloud.com",
        temperature=0.1,
        max_tokens=1024,
    ):
        """
        Get the LLM model
        """
        llm = ChatOCIGenAI(
            model_id=model_id,
            compartment_id=COMPARTMENT_OCID,
            service_endpoint=endpoint,
            model_kwargs={"temperature": temperature, "max_tokens": max_tokens},
        )
        return llm

    def invoke(self, input, config=None, **kwargs):
        """
        Executes the node with APM tracing.

        Args:
            input (Any): The input data for processing.
            config (Optional[Dict]): Optional configuration parameters.
            **kwargs: Additional parameters.

        Returns:
            Any: The output from the subclass-specific `_run_impl()` method.

        Raises:
            Exception: If `_run_impl()` encounters an error.
        """
        # for now config is not used

        # Get subclass name dynamically
        subclass_name = self.__class__.__name__
        # Customize span name
        span_name = f"node_{subclass_name}"

        try:
            with zipkin_span(
                service_name=self.service_name,
                span_name=span_name,
                encoding=Encoding.V2_JSON,
            ):
                logger.info("Calling %s", subclass_name)

                output = self._run_impl(input)

                return output
        except Exception as e:
            logger.error("Error in %s: %s", subclass_name, str(e))
            raise

    @abstractmethod
    def _run_impl(self, _input):
        """
        Subclasses must implement this method to define node execution logic.

        Args:
            _input (Any): Input data to process.

        Returns:
            Any: The processed output.
        """
