"""
OCI Anonymizer
"""

from oci_models import create_model_for_answer_directly
from utils import get_console_logger

logger = get_console_logger()

PROMPT_ANONYMIZER_TEMPLATE = """
    Anonymize the following text by replacing:
    - Client/customer names
    - Company names (different by Oracle)
    - People’s names
    - Emails
    - Language names

    Do NOT anonymize:
    - The word Oracle
    - The document name

    Text to anonymize:
    {text}
    """


class OCIAnonymizer:
    """
    This class provides an anonymizer
    """

    def __init__(self):
        """
        Init
        """
        self.llm = create_model_for_answer_directly()

    def anonymize(self, text: str) -> str:
        """
        anonymize
        """
        PROMPT_ANONYMIZER = PROMPT_ANONYMIZER_TEMPLATE.format(text=text)

        try:
            msg = self.llm.invoke(PROMPT_ANONYMIZER)
            response = msg.content if msg else "Error: No response from LLM"
        except Exception as e:
            logger.error("Summarizer failed: %s", e)
            response = "Error: Unable to process request"

        return response
