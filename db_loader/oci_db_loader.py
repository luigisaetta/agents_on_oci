"""
OCI 23AI DB loader

Utility to read, chunk, embed and load documents in 23AI.
The logic and details for reading and chunking is in load_book_and_split
Currently, based on docling
"""

import os
import oracledb
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.embeddings import OCIGenAIEmbeddings

from config_reader import ConfigReader
from oraclevs_4_db_loading import OracleVS4DBLoading
from chunk_index_utils import load_book_and_split
from config_private import CONNECT_ARGS, COMPARTMENT_OCID
from utils import get_console_logger, compute_stats


# supporting functions
def file_list(directory):
    """
    return the file list in dir
    """
    return [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]


class OCIDBLoader:
    """
    This class provides an implementation of a DB loader
    It:
    - reads documents from a directory provided
    - chunk the documents
    - embeds using OCI Generative AI Ambeddings
    - load in 23AI DB
    Usage:

    """

    def __init__(self):
        """
        Initialize the client
        """
        self.config = ConfigReader("config.toml")
        self.logger = get_console_logger()

    def get_db_connection(self):
        """
        get a connection to db
        """

        self.logger.info("")
        self.logger.info(
            "Connecting as USER: %s to DSN: %s",
            CONNECT_ARGS["user"],
            CONNECT_ARGS["dsn"],
        )

        try:
            return oracledb.connect(**CONNECT_ARGS)
        except oracledb.Error as e:
            self.logger.error("Database connection failed: %s", str(e))
            raise

    def get_embed_model(self):
        """
        get the Embeddings Model
        """
        embed_model_id = self.config.find_key("embed_model_id")
        embed_model_endpoint = self.config.find_key("embed_model_endpoint")

        self.logger.info("")
        self.logger.info("Using embedding model: %s", embed_model_id)
        self.logger.info("")

        embed_model = OCIGenAIEmbeddings(
            auth_type="API_KEY",
            model_id=embed_model_id,
            service_endpoint=embed_model_endpoint,
            compartment_id=COMPARTMENT_OCID,
        )

        return embed_model

    def add_documents(self, books_dir, collection_name):
        """
        read all the documents in books_dir, check if not already
        in the collection. Add the new documents to an existing collection
        """
        max_tokens = self.config.find_key("chunks_max_tokens")

        with self.get_db_connection() as conn:
            # automatically close the conn

            collection_list = OracleVS4DBLoading.list_collections(conn)

            if collection_name not in collection_list:
                self.logger.info("")
                self.logger.error(
                    "Collection %s doesn't exist, exiting!", collection_name
                )
                self.logger.info("")
                return

            # check for existing documents in collection
            books_list = OracleVS4DBLoading.list_books_in_collection(
                connection=conn, collection_name=collection_name
            )

            new_books_list = file_list(books_dir)

            docs = []

            for book_name in new_books_list:
                # check if already loaded

                # strips path
                if book_name not in books_list:
                    self.logger.info("Loading %s", book_name)

                    docs += load_book_and_split(books_dir, book_name, max_tokens)

                else:
                    self.logger.info(
                        "Document %s already loaded, skipping...", book_name
                    )

            # embed and save to  DB
            if len(docs) > 0:
                embed_model = self.get_embed_model()

                self.manage_collection(
                    conn, docs, embed_model, collection_name, is_new=False
                )

                self.logger.info("Loading completed.")
                self.logger.info("")

                _mean, _stdev, _perc_75 = compute_stats(docs)
                self.log_stats(
                    n_chunks=len(docs), mean=_mean, stdev=_stdev, perc_75=_perc_75
                )

    def from_documents(self, books_dir, collection_name):
        """
        create anew collection and add the docs in cooks_dir
        """
        max_tokens = self.config.find_key("chunks_max_tokens")

        with self.get_db_connection() as conn:
            collection_list = OracleVS4DBLoading.list_collections(conn)

            # check that the collection doens't exist yet
            if collection_name in collection_list:
                self.logger.info("")
                self.logger.error(
                    "Collection %s alredy exist, exiting!", collection_name
                )
                self.logger.info("")
                return

            # ok, collection is new
            new_books_list = file_list(books_dir)

            docs = []

            for book_name in new_books_list:
                # strips path
                self.logger.info("Loading %s", book_name)

                docs += load_book_and_split(books_dir, book_name, max_tokens)

            # embed and save to  DB
            if len(docs) > 0:
                embed_model = self.get_embed_model()

                # create collection and load
                self.manage_collection(
                    conn, docs, embed_model, collection_name, is_new=True
                )

                self.logger.info("Loading completed.")
                self.logger.info("")

                _mean, _stdev, _perc_75 = compute_stats(docs)
                self.log_stats(
                    n_chunks=len(docs), mean=_mean, stdev=_stdev, perc_75=_perc_75
                )

    def manage_collection(self, conn, docs, embed_model, collection_name, is_new):
        """
        Create or update a collection in the 23AI vector store.
        """
        if is_new:
            self.logger.info(
                "Creating collection '%s' and adding documents...", collection_name
            )
            OracleVS4DBLoading.from_documents(
                docs,
                embed_model,
                client=conn,
                table_name=collection_name,
                distance_strategy=DistanceStrategy.COSINE,
            )
        else:
            self.logger.info(
                "Updating existing collection '%s' with new documents...",
                collection_name,
            )
            v_store = OracleVS4DBLoading(
                client=conn,
                table_name=collection_name,
                distance_strategy=DistanceStrategy.COSINE,
                embedding_function=embed_model,
            )
            v_store.add_documents(docs)

        self.logger.info("Operation completed for collection: %s", collection_name)

    def close_db_connection(self, conn):
        """
        close the D connection
        """
        try:
            conn.close()
        except oracledb.Error:
            pass

    def delete_documents_in_collection(self, collection_name, doc_names: list):
        """
        drop documents in the given collection
        """
        if len(doc_names) > 0:
            with self.get_db_connection() as conn:
                self.logger.info(
                    "Delete docs: %s in collection %s", doc_names, collection_name
                )
                OracleVS4DBLoading.delete_documents(conn, collection_name, doc_names)

    # helper
    def log_stats(self, n_chunks, mean, stdev, perc_75):
        """
        log the stats on the distribuction of chunks lenghts
        """
        self.logger.info("")
        self.logger.info("Statistics on the distribution of chunk lengths:")
        self.logger.info("Total num. of chunks loaded: %s", n_chunks)
        self.logger.info("Avg. length: %s (chars)", mean)
        self.logger.info("Std dev: %s (chars)", stdev)
        self.logger.info("75-perc: %s (chars)", perc_75)
        self.logger.info("")
