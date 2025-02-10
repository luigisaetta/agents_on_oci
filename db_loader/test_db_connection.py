"""
Test connection to Vector Store
"""

from oci_db_loader import OCIDBLoader
from utils import get_console_logger

logger = get_console_logger()

try:
    loader = OCIDBLoader()

    with loader.get_db_connection() as conn:
        logger.info("")
        logger.info("Connection OK")
        logger.info("")

except Exception as e:
    logger.error("Error testing connection...")
    logger.error(e)
