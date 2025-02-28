"""
Class to handle places info request
"""
from agent_base_node import BaseAgentNode
from langchain_core.messages import HumanMessage, SystemMessage

from config_reader import ConfigReader
from prompts_library import PROMPT_PLACES_INFO

config = ConfigReader("config.toml")
AD_MODEL_ID = config.find_key("ad_model_id")

class PlacesInfo(BaseAgentNode):
    """
    This is the class to get places info.

    It is derived from BaseTracingNode, therefore supports tracing to OCI APM
    """

    def _run_impl(self, state):
        """Subclasses must implement this method."""

        # Generate section
        # we're using another model
        llm = self.get_llm_model(model_id=AD_MODEL_ID, temperature=0.1, max_tokens=2048)
        
        messages = [
            SystemMessage(content=PROMPT_PLACES_INFO),
            HumanMessage(content=state["input"]),
        ]

        result = llm.invoke(input=messages)

        return {"output": result.content, "output_tool": "places_info"}