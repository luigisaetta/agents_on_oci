"""
Goal Analyzer
"""

import sys
import os

# to be able to import from parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from agent_base_node import BaseAgentNode


class GoalAnalyzer(BaseAgentNode):
    def _run_impl(self, state):
        """Third LLM call to analyze goals"""

        llm = self.get_llm_model(max_tokens=2048)

        request = f"""Evaluate the following text: {state['file_text']}.
        Check that it defines clear and measurable goals.
        Provide a score ranging from 1 to 10 (10 is best).
        """

        msg = llm.invoke(request)

        return {"output3": msg.content}
