"""
router.py
"""

from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage

from oci_models import create_model_for_routing
from prompts_library import PROMPT_ROUTER
from utils import get_console_logger

#
# json schema for the output of the Router
# needs to be adapted to the actual output
#
# TODO: can be generalized passing the list of outcomes
json_route = {
    "title": "Route",
    "description": "Defines the output of the routing logic",
    "type": "object",
    "properties": {
        "step": {
            "description": "The next step in the routing process",
            "type": "string",
            "enum": [
                "generate_sql",
                "not_allowed",
                "analyze_data",
                "answer_directly",
                "not_defined",
            ],
        }
    },
    "required": ["step"],
}


# State: the input to the agent
class State(TypedDict):
    """
    Defines the internal state of the agent
    """

    input: str
    decision: str
    output: str


class Router:
    """
    This class provides a router for the agent
    """

    def __init__(self):
        """
        Initialize the router
        """
        self.logger = get_console_logger()
        self.llm_router = create_model_for_routing()
        self.router = self.llm_router.with_structured_output(json_route)

    def route(self, state: State) -> dict:
        """
        Route the input to the appropriate agent

        :param input: the input to the agent
        :return: the output from the agent
        """
        self.logger.info("Called router...")

        # Run the augmented LLM with structured output to serve as routing logic
        decision = self.router.invoke(
            [
                HumanMessage(content=PROMPT_ROUTER + state["input"]),
            ]
        )

        self.logger.info("Decision: %s", decision)

        return {"decision": decision["step"]}
