"""
Class to handle request for meeting info
"""

import sys
import os

# to be able to import from parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from langchain_core.messages import HumanMessage, SystemMessage

from agent_base_node import BaseAgentNode
from utils import extract_dates_from_json_string
from meetings_api import appointments_dict, find_free_slots


class MeetingsInfo(BaseAgentNode):
    """
    This is the class to get meeting info, free slots.

    It is derived from BaseTracingNode, therefore supports tracing to OCI APM
    """

    PROMPT_MEETINGS_INFO = """
    You are an intelligent assistant that extracts date information from user queries about free slots or meetings. 
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

    ### **Output Format (JSON):**
    ```json
    {
        "start_date": "YYYY-MM-DD" or null,
        "end_date": "YYYY-MM-DD" or null
    }

    """

    def _run_impl(self, state):
        """Subclasses must implement this method."""

        # Generate section
        # we're using another model
        llm = self.get_llm_model(temperature=0.1, max_tokens=2048)

        messages = [
            SystemMessage(content=self.PROMPT_MEETINGS_INFO),
            HumanMessage(content=state.input),
        ]

        result = llm.invoke(input=messages)

        start_date, end_date = extract_dates_from_json_string(result.content)

        free_slots = find_free_slots(
            appointments_dict["appointments"], start_date, end_date
        )

        state.output = str(free_slots)

        return state
