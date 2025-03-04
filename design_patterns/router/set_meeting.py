"""
Class to handle set_meeting command
"""

import sys
import os

# to be able to import from parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from pydantic import BaseModel
from typing import Optional
from langchain_core.messages import HumanMessage, SystemMessage

from agent_base_node import BaseAgentNode
from structured_llm import StructuredLLM
from meetings_api import appointments_dict, set_appointment
from utils import extract_meeting_details


class SetMeetingsInfoState(BaseModel):
    """
    Defines the result of the parsing of LLM output.
    """

    date: Optional[str] = None
    start_hour: Optional[str] = None
    end_hour: Optional[str] = None


class SetMeeting(BaseAgentNode):
    """
    This is the class to get meeting info, free slots.

    It is derived from BaseTracingNode, therefore supports tracing to OCI APM
    """

    GENERAL_INFO = """
    Extracts date information from user queries about setting up a meeting. 
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

    """

    def _run_impl(self, state):
        """Subclasses must implement this method."""

        # Generate section
        # we're using another model
        llm = StructuredLLM(
            model=SetMeetingsInfoState, general_instructions=self.GENERAL_INFO
        )

        result = llm.invoke(state.input)
        # result is of type SetMeetingsInfoState

        print(result)

        set_appointment(
            result.date,
            result.start_hour,
            result.end_hour,
            participants="",
            notes="Set by AI",
        )

        state.output = f"meeting set on {result.date} from {result.start_hour} to {result.end_hour}"

        return state
