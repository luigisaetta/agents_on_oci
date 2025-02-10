"""
create a new collection and load documents
"""

import argparse

from oci_db_loader import OCIDBLoader

parser = argparse.ArgumentParser(description="Document batch loading.")

parser.add_argument(
    "collection_name", type=str, help="collection name to add documents to."
)
parser.add_argument("books_dir", type=str, help="Dir with the books to load.")

args = parser.parse_args()
collection_name = args.collection_name
books_dir = args.books_dir

loader = OCIDBLoader()

# check that the collection is new, create it and load documents chunked
loader.from_documents(books_dir, collection_name)

print("")
