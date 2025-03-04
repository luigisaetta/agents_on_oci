"""
Class to handle request for meeting info

Updates:
- 2025-03-04: Added structured LLM
"""

import sys
import os

# to be able to import from parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from pydantic import BaseModel
from typing import Optional

from agent_base_node import BaseAgentNode
from structured_llm import StructuredLLM
from meetings_api import appointments_dict, find_free_slots


class MeetingsInfoState(BaseModel):
    """
    Defines the result of the parsing of LLM output.
    """

    start_date: Optional[str] = None
    end_date: Optional[str] = None


class MeetingsInfo(BaseAgentNode):
    """
    This is the class to get meeting info, free slots.

    It is derived from BaseTracingNode, therefore supports tracing to OCI APM
    """

    # this is passed to the StructuredLLM as general info
    GENERAL_INFO = """
    Extracts date information from user queries about free slots in the agenda or meetings. 
    Given a user query, your task is to extract the **start date** and **end date** related to the request. 
    The dates should be formatted as `"YYYY-MM-DD"`. 

    If the user provides only one date, set the **other date as `null`** in the output.

    ### **Guidelines:**
    - The input may contain a **specific date (e.g., "2025-02-10")** or a **date range (e.g., "from 2025-02-10 to 2025-02-15")**.
    - The input may also include **relative dates** like:
    - `"today"`, `"tomorrow"`, `"yesterday"`
    - `"next Monday"`, `"last Friday"`
    - `"this week"`, `"next week"`, `"last month"`
    - Convert all dates to **ISO format (`YYYY-MM-DD`)**.
    - If the user mentions a **single date**, return `"end_date": null`.
    - If no date is found, return both values as `null`.

    """

    def _run_impl(self, state):
        """Subclasses must implement this method."""

        llm = StructuredLLM(
            model=MeetingsInfoState, general_instructions=self.GENERAL_INFO
        )

        result = llm.invoke(state.input)
        # result is of type MeetingsInfoState

        # call the meetings api to find free slots
        free_slots = find_free_slots(
            appointments_dict["appointments"], result.start_date, result.end_date
        )

        state.output = str(free_slots)

        return state
