"""
Generic class for adding APM tracing
"""

from abc import ABC, abstractmethod
from langchain_core.runnables import Runnable

# added to integrate with APM
from py_zipkin import Encoding
from py_zipkin.zipkin import zipkin_span


SERVICE_NAME = "agents01"


class BaseNode(Runnable, ABC):
    """
    This class is a base class for all nodes in the pipeline.
    It provides a common interface for running a node and a hook for adding
    custom logic
    """

    def invoke(self, input, config=None, **kwargs):
        """Wrap execution with APM tracing dynamically based on subclass name"""

        # Get subclass name dynamically
        subclass_name = self.__class__.__name__
        # Customize span name
        span_name = f"node_{subclass_name}"

        with zipkin_span(
            service_name=SERVICE_NAME, span_name=span_name, encoding=Encoding.V2_JSON
        ):
            # Common pre-run logic (if any)

            result = self._run_impl(input)

            # Common post-run logic (if any)
            return result

    @abstractmethod
    def _run_impl(self, input):
        """Subclasses must implement this method."""
