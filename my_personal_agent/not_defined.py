"""
Class to handle the not_defined case
"""

from langchain_core.messages import HumanMessage, SystemMessage

from agent_base_node import BaseAgentNode
from config_reader import ConfigReader
from prompts_library import PROMPT_NOT_DEFINED

config = ConfigReader("config.toml")
AD_MODEL_ID = config.find_key("ad_model_id")


class NotDefined(BaseAgentNode):
    """
    This is the class to handle the not_defined case

    It is derived from BaseTracingNode, therefore supports tracing to OCI APM
    """

    def _run_impl(self, state):
        """Subclasses must implement this method."""

        # Generate section
        # we're using another model
        llm = self.get_llm_model(model_id=AD_MODEL_ID, temperature=0.1, max_tokens=2048)

        messages = [
            SystemMessage(content=PROMPT_NOT_DEFINED),
            HumanMessage(content=state["input"]),
        ]

        result = llm.invoke(input=messages)

        return {"output": result.content, "output_tool": "not_defined"}
