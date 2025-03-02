"""
Aggregator
"""

import sys
import os

# to be able to import from parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from agent_base_node import BaseAgentNode


class Aggregator(BaseAgentNode):
    def _run_impl(self, state):
        """Combine all the outputs from steps into a single output"""

        # here we can add whatever logic we want,
        combined = f"## Analysis of the document: {state['file_name']}\n\n"
        combined += f"### Summary:\n{state['output4']}\n\n"
        combined += f"### Clarity:\n{state['output2']}\n\n"
        combined += f"### Goals:\n{state['output3']}\n\n"
        combined += f"### Spelling errors:\n{state['output1']}\n\n"

        return {"combined_output": combined}
