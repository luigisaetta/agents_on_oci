"""
Class to handle set_meeting command
"""

import sys
import os

# to be able to import from parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from langchain_core.messages import HumanMessage, SystemMessage

from agent_base_node import BaseAgentNode
from meetings_api import appointments_dict, set_appointment
from utils import extract_meeting_details


class SetMeeting(BaseAgentNode):
    """
    This is the class to get meeting info, free slots.

    It is derived from BaseTracingNode, therefore supports tracing to OCI APM
    """

    PROMPT_SET_MEETING = """
    You are an intelligent assistant that extracts date information from user queries about setiing up a meeting. 
    Given a user query, your task is to extract the **date** and **start hour** and **end hour** related to the request. 
    The dates should be formatted as `"YYYY-MM-DD"`.
    Hour should be formatted as `"HH:MM"`.

    ### **Guidelines:**
    - The input must contain a **specific date (e.g., "2025-02-10")** and **start hour** and **end hour**.
    - The input date may also include **relative dates** like:
    - `"today"`, `"tomorrow"`, `"yesterday"`
    - `"next Monday"`, `"last Friday"`
    - Convert all dates to **ISO format (`YYYY-MM-DD`)**.
    - If no date is found, return  `null`.
    - if no start hour is found, return `null`.
    - if no end hour is found, return `null`.

    ### **Output Format (JSON):**
    ```json
    {
        "date": "YYYY-MM-DD" or null,
        "start_hour": "HH:MM" or null,
        "end_hour": "HH:MM" or null
    }

    """

    def _run_impl(self, state):
        """Subclasses must implement this method."""

        # Generate section
        # we're using another model
        llm = self.get_llm_model(temperature=0, max_tokens=1024)

        messages = [
            SystemMessage(content=self.PROMPT_SET_MEETING),
            HumanMessage(content=state.input),
        ]

        result = llm.invoke(input=messages)

        print(result.content)

        # parse it
        parse_result = extract_meeting_details(result.content)
        
        print(parse_result)
        
        date = parse_result["date"]
        start_hour = parse_result["start_hour"]
        end_hour = parse_result["end_hour"]

        set_appointment(date, start_hour, end_hour, participants="", notes="Set by AI")

        state.output = f"meeting set on {date} from {start_hour} to {end_hour}"

        return state
