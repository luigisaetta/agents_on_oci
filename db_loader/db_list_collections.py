"""
Print the list of collections in the schema
"""

from oci_db_loader import OCIDBLoader
from oraclevs_4_db_loading import OracleVS4DBLoading

from utils import get_console_logger

# handle input for collection_name from command line
logger = get_console_logger()

loader = OCIDBLoader()

with loader.get_db_connection() as conn:
    coll_list = OracleVS4DBLoading.list_collections(conn)

logger.info("")
logger.info("List of collections:")
logger.info("")

for coll in coll_list:
    logger.info("* %s", coll)

logger.info("")
