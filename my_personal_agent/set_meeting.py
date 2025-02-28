"""
Class to handle set_meeting command
"""

from langchain_core.messages import HumanMessage, SystemMessage

from agent_base_node import BaseAgentNode
from config_reader import ConfigReader

config = ConfigReader("config.toml")
AD_MODEL_ID = config.find_key("ad_model_id")


class SetMeeting(BaseAgentNode):
    """
    This is the class to get meeting info, free slots.

    It is derived from BaseTracingNode, therefore supports tracing to OCI APM
    """

    def _run_impl(self, state):
        """Subclasses must implement this method."""

        # Generate section
        # we're using another model
        llm = self.get_llm_model(model_id=AD_MODEL_ID, temperature=0.1, max_tokens=2048)

        return {"output": "meeting set", "output_tool": "set_meeting"}
