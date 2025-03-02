"""
Clarity Analyzer
"""

import sys
import os

# to be able to import from parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from agent_base_node import BaseAgentNode


class ClarityAnalyzer(BaseAgentNode):
    def _run_impl(self, state):
        """Second LLM call to analyze clarity"""

        llm = self.get_llm_model(max_tokens=2048)

        request = f"""Evaluate from the point of view of clarity the following text: {state['file_text']}.
        Provide a score ranging from 1 to 10 (10 is best).
        """

        msg = llm.invoke(request)

        return {"output2": msg.content}
