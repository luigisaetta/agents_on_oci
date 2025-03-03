"""
Router implementation based on llm_structured
"""

from structured_llm import StructuredLLM


class Router(StructuredLLM):
    """
    This class implement a router using Llama 3.3, using the example StructuredLLM
    """

    def route(self, state: type) -> dict:
        """
        Route the user input to the correct endpoint

        state: the state of the workflow
        """
        new_state = self.invoke(state.input)

        return new_state
