"""
The aggregator
"""

import sys
import os

# to be able to import from parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from langchain_core.messages import HumanMessage, SystemMessage

from agent_base_node import BaseAgentNode
from utils import get_console_logger

logger = get_console_logger()


class Aggregator(BaseAgentNode):
    """
    Generate the final output
    """

    def _run_impl(self, state):
        """Subclasses must implement this method."""
        # for now, only logging
        logger.info("aggregator: Aggregating outputs...")

        # would need to work on state output

        return state
