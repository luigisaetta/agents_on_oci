"""
Prototype for structured output with Llama 3.3
"""

from typing import List, Optional
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_community.chat_models import ChatOCIGenAI
from config_private import COMPARTMENT_OCID


class StructuredLLM:
    """
    A reusable class for generating structured responses from an LLM
    using LCEL (LangChain Expression Language).

    This class integrates:
    - A Pydantic model to enforce structured output.
    - Few-shot learning examples (optional) to guide response format.
    - An LLM model (Llama 3.3 on OCI) via LangChain.

    It ensures that the model outputs JSON data matching the given Pydantic schema.

    Attributes:
        parser (PydanticOutputParser): Parses LLM responses into structured output.
        format_instructions (str): Instructions for enforcing JSON output.
        few_shot_examples (str): Examples formatted for the prompt (optional).
        prompt (PromptTemplate): The structured prompt.
        llm_model_name (str): LLM model name (e.g., Llama 3.3).
        llm_endpoint (str): API endpoint for the LLM.

    Methods:
        invoke(user_input: str) -> Pydantic Model:
            Sends user input to the LLM and returns a structured response.

    Example:
        >>> from pydantic import BaseModel
        >>> class JokeResponse(BaseModel):
        ...     setup: str
        ...     punchline: str
        >>> few_shots = [
        ...     {"input": "Tell me a joke about AI",
                "output": {"setup": "Why did the AI cross the road?",
                "punchline": "To optimize its neural network!"}},
        ...     {"input": "Tell me a joke about Python",
                "output": {"setup": "Why do Python developers prefer spaces?",
                "punchline": "Because they hate tabs!"}},
        ... ]
        >>> structured_llm = StructuredLLM(model=JokeResponse, few_shot_examples=few_shots)
        >>> response = structured_llm.invoke("Tell me a joke about data science.")
        >>> print(response)
        JokeResponse(setup="Why did the data scientist break up with the statistician?",
                     punchline="Because he needed more confidence in the relationship!")
    """

    def __init__(
        self,
        model: type,
        llm_model_name: str = "meta.llama-3.3-70b-instruct",
        llm_endpoint: str = "https://inference.generativeai.eu-frankfurt-1.oci.oraclecloud.com",
        few_shot_examples: Optional[List[dict]] = None,
    ):
        """
        Initializes an LLM with structured output support.

        Args:
        - model (type): A Pydantic model defining the expected output schema.
        - llm_model_name (str, optional): Name of the LLM to use. Defaults to Llama 3.3.
        - llm_endpoint (str, optional): API endpoint for LLM.
        - few_shot_examples (list of dict, optional): A list of few-shot examples.
          Each example must have:
            - "input": Example user input.
            - "output": Example expected structured response.
        """
        self.parser = PydanticOutputParser(pydantic_object=model)
        self.format_instructions = self.parser.get_format_instructions()
        self.llm_model_name = llm_model_name
        self.llm_endpoint = llm_endpoint

        # Process few-shot examples into a formatted string
        self.few_shot_examples = ""
        if few_shot_examples:
            self.few_shot_examples = "\n".join(
                [
                    f"Example:\nUser Input: {ex['input']}\nAI Output:\n{ex['output']}"
                    for ex in few_shot_examples
                ]
            )

        # Define structured prompt with format instructions and optional few-shot examples
        self.prompt = PromptTemplate(
            template=(
                "You are a helpful AI assistant. "
                "You must return a JSON object that strictly follows this schema:\n"
                "{format_instructions}\n"
                "{few_shot_examples}\n"
                "Make sure your response is valid JSON without additional text.\n"
                "User Input: {input}"
            ),
            input_variables=["input"],
            partial_variables={
                "format_instructions": self.format_instructions,
                "few_shot_examples": self.few_shot_examples,
            },
        )

    def get_chain(self):
        """
        Returns:
         - the LLM chain

        Note:
        to avoid caching the LLM connection.
        """
        # Define the LLM
        llm = ChatOCIGenAI(
            model_id=self.llm_model_name,
            compartment_id=COMPARTMENT_OCID,
            service_endpoint=self.llm_endpoint,
            model_kwargs={"temperature": 0, "max_tokens": 1024},
        )

        # Create the LCEL pipeline
        chain = self.prompt | llm | self.parser

        return chain

    def invoke(self, user_input: str):
        """
        Invokes the structured LLM pipeline.

        Args:
        - user_input (str): The input prompt/question.

        Returns:
        - Parsed structured response based on the given Pydantic model.
        """
        return self.get_chain().invoke({"input": user_input})
