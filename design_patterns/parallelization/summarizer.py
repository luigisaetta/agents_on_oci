"""
Summarizer
"""

import sys
import os

# to be able to import from parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from agent_base_node import BaseAgentNode


class Summarizer(BaseAgentNode):
    def _run_impl(self, state):
        """Fourth LLM call to summarize"""

        llm = self.get_llm_model(max_tokens=2048)

        request = f"""Summarize the following text in one page: {state['file_text']}.
        """

        msg = llm.invoke(request)

        return {"output4": msg.content}
