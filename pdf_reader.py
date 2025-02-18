"""
PDF Reader

Note: for now, it is based on pdfplumber
"""

import pdfplumber

from utils import get_console_logger


class PDFReader:
    """
    Read and extract only the text from a pdf
    """

    def __init__(self, file_path):
        """
        Initializes the PDF reader and loads the file into memory.
        :param file_path: Path to the PDF file
        """
        self.file_path = file_path
        self.text = None
        self.logger = get_console_logger()

    def load_file(self):
        """
        Reads the PDF file and extracts the text.
        """
        try:
            with pdfplumber.open(self.file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text()
            self.text = text
        except FileNotFoundError:
            self.logger.error("Error: The file %s does not exist.", self.file_path)
            self.text = ""
        except Exception as e:
            self.logger.error("Error while reading the PDF file: %s", e)
            self.text = ""

    def get_text(self):
        """
        Returns the text extracted from the PDF file.
        :return: The text extracted from the PDF file
        """
        return self.text
