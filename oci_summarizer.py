"""
OCI Summarizer
"""
from oci_models import create_model_for_answer_directly
from utils import get_console_logger

logger = get_console_logger()

PROMPT_SUMMARIZER_TEMPLATE = """
    You are an expert summarizer with strong analytical skills. 
    Your task is to generate a **clear, concise, and well-structured** summary of the following text.

    ### **Instructions:**
    - Summarize the text in a way that captures its **main ideas, key points, and essential details**.
    - Keep the summary **within one page** (approximately **250-300 words**).
    - Maintain **logical flow and coherence** in the summary.
    - Preserve the **original intent and meaning** while using **clear and concise language**.
    - Avoid unnecessary details, repetitions, or excessive examples.

    ### **Text to Summarize:**
    {text}

    ### **Expected Response Format:**
    **Summary:**  
    [Well-structured and concise summary, approximately 250-300 words]  
    """

class OCISummarizer:
    """
    This class provides a summarizer
    """

    def __init__(self):
        """
        Init
        """
        self.llm = create_model_for_answer_directly()
    
    def summarize(self, text:str) -> str:
        PROMPT_SUMMARIZER = PROMPT_SUMMARIZER_TEMPLATE.format(text=text)
        
        try:
            msg = self.llm.invoke(PROMPT_SUMMARIZER)
            response = msg.content if msg else "Error: No response from LLM"
        except Exception as e:
            logger.error("Summarizer failed: %s", e)
            response = "Error: Unable to process request"

        return response
        
