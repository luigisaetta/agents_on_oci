"""
Test connection to Vector Store
"""

from db_doc_loader_backend import get_db_connection
from utils import get_console_logger

logger = get_console_logger()

try:
    with get_db_connection() as conn:
        logger.info("")
        logger.info("Connection OK")
        logger.info("")

except Exception as e:
    logger.error("Error testing connection...")
    logger.error(e)
