"""
File Reader
"""

import re
import pdfplumber

import sys
import os

from langchain_core.messages import HumanMessage, SystemMessage

# to be able to import from parent directory
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

from agent_base_node import BaseAgentNode
from utils import get_console_logger

logger = get_console_logger()


class FileReader(BaseAgentNode):
    # helper functions
    def extract_file_name(self, text):
        match = re.search(r"```(.*?)```", text)
        if match:
            return match.group(1)
        return None

    def read_pdf(self, file_name):
        testo = ""
        with pdfplumber.open(file_name) as pdf:
            for pagina in pdf.pages:
                testo += pagina.extract_text() + "\n"
        return testo

    def _run_impl(self, state):
        """
        Extract the file name and read it
        """

        PROMPT = """
        Analyze the user's request and extract only the file name.
        Provide only the file name enclosed in triple backtick.
        """
        llm = self.get_llm_model(temperature=0.0)

        messages = [
            SystemMessage(content=PROMPT),
            HumanMessage(content=state["request"]),
        ]

        result = llm.invoke(input=messages)

        f_name = self.extract_file_name(result.content)
        logger.info(f"File name to be analyzed is: {f_name}")

        logger.info("Reading file content...")
        file_text = self.read_pdf(f_name)

        return {"file_name": f_name, "file_text": file_text}
