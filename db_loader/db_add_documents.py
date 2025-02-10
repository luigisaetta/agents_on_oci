"""
Load additional docs in an existing collection

refactored to use oci_db_loader
"""

import argparse
from oci_db_loader import OCIDBLoader

from config_reader import ConfigReader
from utils import get_console_logger

# handle input for collection_name from command line
logger = get_console_logger()
config = ConfigReader("config.toml")

parser = argparse.ArgumentParser(description="Document batch loading.")

parser.add_argument(
    "collection_name", type=str, help="collection name to add documents to."
)
parser.add_argument("books_dir", type=str, help="Dir with the books to load.")

args = parser.parse_args()
collection_name = args.collection_name
books_dir = args.books_dir

logger.info("")
logger.info("Input dir: %s", books_dir)
logger.info("Target collection: %s", collection_name)

# the component for DB loading
oci_loader = OCIDBLoader()

oci_loader.add_documents(books_dir, collection_name)

print("")
