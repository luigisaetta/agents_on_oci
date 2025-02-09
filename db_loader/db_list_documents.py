"""
Print the list of documents in the collection
"""

import argparse

from db_doc_loader_backend import get_db_connection
from oraclevs_4_db_loading import OracleVS4DBLoading

from utils import get_console_logger

# handle input for collection_name from command line
logger = get_console_logger()

parser = argparse.ArgumentParser(description="Document batch loading.")

parser.add_argument("collection_name", type=str, help="collection name.")

args = parser.parse_args()
collection_name = args.collection_name

with get_db_connection() as conn:
    docs_list = OracleVS4DBLoading.list_books_in_collection(conn, collection_name)

logger.info("")
logger.info("List of documents in collection %s", collection_name)
logger.info("")

for doc in docs_list:
    logger.info("* %s", doc)

logger.info("")
