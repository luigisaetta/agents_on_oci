"""
Class to handle request for meeting info
"""
from agent_base_node import BaseAgentNode
from langchain_core.messages import HumanMessage, SystemMessage

from config_reader import ConfigReader
from prompts_library import PROMPT_MEETINGS_INFO
from utils import extract_dates_from_json_string
from meetings_api import appointments_dict, find_free_slots

config = ConfigReader("config.toml")
AD_MODEL_ID = config.find_key("ad_model_id")

class MeetingInfo(BaseAgentNode):
    """
    This is the class to get meeting info, free slots.

    It is derived from BaseTracingNode, therefore supports tracing to OCI APM
    """

    def _run_impl(self, state):
        """Subclasses must implement this method."""

        # Generate section
        # we're using another model
        llm = self.get_llm_model(model_id=AD_MODEL_ID, temperature=0.1, max_tokens=2048)
        
        messages = [
            SystemMessage(content=PROMPT_MEETINGS_INFO),
            HumanMessage(content=state["input"]),
        ]

        result = llm.invoke(input=messages)
        
        start_date, end_date = extract_dates_from_json_string(result.content)

        free_slots = find_free_slots(appointments_dict["appointments"], start_date, end_date)
    
        return {"output": str(free_slots), "output_tool": "meetings_info"}