"""
Error identifier
"""

import sys
import os

parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from agent_base_node import BaseAgentNode


class ErrorIdentifier(BaseAgentNode):
    def _run_impl(self, state):
        """LLM call to generate spelling errors list"""
        TOP_E = 10

        llm = self.get_llm_model(max_tokens=2048)

        request = f"Identify top {TOP_E} spelling errors in the following text: {state['file_text']}"
        msg = llm.invoke(request)

        return {"output1": msg.content}
