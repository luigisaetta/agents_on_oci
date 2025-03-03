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


class SetMeeting(BaseAgentNode):
    """
    This is the class to get meeting info, free slots.

    It is derived from BaseTracingNode, therefore supports tracing to OCI APM
    """

    def _run_impl(self, state):
        """Subclasses must implement this method."""

        # Generate section
        # we're using another model
        llm = self.get_llm_model(temperature=0.1, max_tokens=2048)

        return {"output": "meeting set", "output_tool": "set_meeting"}
