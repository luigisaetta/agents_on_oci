"""
Load additional docs in an existing collection
"""

import sys
import os
import argparse

from db_doc_loader_backend import (
    get_list_collections,
    get_books,
    manage_collection,
    get_embed_model,
)
from chunk_index_utils import load_book_and_split
from utils import get_console_logger, compute_stats
from config_reader import ConfigReader


def file_list(directory):
    """
    return the file list in dir
    """
    return [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]


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
max_tokens = config.find_key("chunks_max_tokens")

# check if collection exist
collection_list = get_list_collections()

if collection_name not in collection_list:
    logger.info("")
    logger.error("Collection %s doesn't exist, exiting!", collection_name)
    logger.info("")

    sys.exit(-1)

# check for existing documents in collection
books_list = get_books(collection_name)

new_books_list = file_list(books_dir)

logger.info("")

docs = []

for book_name in new_books_list:
    # check if already loaded

    # strips path
    if book_name not in books_list:
        logger.info("Loading %s", book_name)

        docs += load_book_and_split(books_dir, book_name, max_tokens)

    else:
        logger.info("Document %s already loaded, skipping...", book_name)

# embed and save to  DB
if len(docs) > 0:
    embed_model = get_embed_model()

    manage_collection(docs, embed_model, collection_name, is_new_collection=False)

    logger.info("Loading completed.")
    logger.info("")

    mean, stdev, perc_75 = compute_stats(docs)

    logger.info("")
    logger.info("Statistics on the distribution of chunk lengths:")
    logger.info("Total num. of chunks loaded: %s", len(docs))
    logger.info("Avg. length: %s (chars)", mean)
    logger.info("Std dev: %s (chars)", stdev)
    logger.info("75-perc: %s (chars)", perc_75)
    logger.info("")
