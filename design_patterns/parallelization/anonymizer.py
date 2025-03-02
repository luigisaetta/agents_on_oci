"""
Anonymizer
"""

import sys
import os

# to be able to import from parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from agent_base_node import BaseAgentNode


class Anonymizer(BaseAgentNode):
    def _run_impl(self, state):
        """LLM call to anonymize"""

        # needs more tokens since works on the aggregation
        llm = self.get_llm_model(max_tokens=2048)

        request = f"""Anonymize the following text replacing client/customer name, people names, emails.
        Don't anonymize: the document name.
        Text: {state['combined_output']}.
        """

        msg = llm.invoke(request)

        return {"final_output": msg.content}
