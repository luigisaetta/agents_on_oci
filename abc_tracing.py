"""
Generic class for adding APM tracing
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


class BaseTracingNode(Runnable, ABC):
    """
    This class is a base class for all nodes in the agent
    where you equip the node with APM tracing capabilities.
    It provides a common interface for running a node and a hook for adding
    custom logic
    """

    def __init__(self, service_name="test01", json_schema=None):
        """
        Init the node with service name and json schema
        """
        self.service_name = service_name
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
        Wrap execution with APM tracing dynamically
        based on subclass name
        """
        # for now config is not used

        # Get subclass name dynamically
        subclass_name = self.__class__.__name__
        # Customize span name
        span_name = f"node_{subclass_name}"

        with zipkin_span(
            service_name=self.service_name,
            span_name=span_name,
            encoding=Encoding.V2_JSON,
        ):
            # Common pre-run logic (if any)
            logger.info("Calling %s", subclass_name)

            output = self._run_impl(input)

            # Common post-run logic (if any)
            return output

    @abstractmethod
    def _run_impl(self, input):
        """
        Subclasses must implement this method.

        IN the method implementation you can call get_llm_model
        to get the LLM model
        """
