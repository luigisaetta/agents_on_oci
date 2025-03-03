"""
Class to handle the not_defined case
"""

import sys
import os

# to be able to import from parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from langchain_core.messages import HumanMessage, SystemMessage

from agent_base_node import BaseAgentNode


class NotDefined(BaseAgentNode):
    """
    This is the class to handle the not_defined case

    It is derived from BaseTracingNode, therefore supports tracing to OCI APM
    """

    PROMPT_NOT_DEFINED = """
    You are an AI assistant that can help users to clarify what they can ask for.
    Report always the user question.
    Use always a formal and professional tone.
    If you don't have all the information to answer ask for more information.
    Format the response in markdown.

    """

    def _run_impl(self, state):
        """Subclasses must implement this method."""

        # Generate section
        # we're using another model
        llm = self.get_llm_model(temperature=0.1, max_tokens=2048)

        messages = [
            SystemMessage(content=self.PROMPT_NOT_DEFINED),
            HumanMessage(content=state.input),
        ]

        result = llm.invoke(input=messages)

        state.output = result.content

        return state
