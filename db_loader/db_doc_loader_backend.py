"""
Docs loader backend function

to separate UI logic from backend logic
"""

import oracledb

from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.embeddings import OCIGenAIEmbeddings
from oraclevs_4_db_loading import OracleVS4DBLoading
from utils import get_console_logger

from chunk_index_utils import (
    load_book_and_split,
)

from config_reader import ConfigReader
from config_private import CONNECT_ARGS, COMPARTMENT_OCID

logger = get_console_logger()

config = ConfigReader("config.toml")


def get_db_connection():
    """
    get a connection to db
    """

    logger.info("")
    logger.info(
        "Connecting as USER: %s to DSN: %s", CONNECT_ARGS["user"], CONNECT_ARGS["dsn"]
    )

    try:
        return oracledb.connect(**CONNECT_ARGS)
    except oracledb.Error as e:
        logger.error("Database connection failed: %s", str(e))
        raise


def get_embed_model():
    """
    get the Embeddings Model
    """
    embed_model_id = config.find_key("embed_model_id")
    embed_model_endpoint = config.find_key("embed_model_endpoint")

    logger.info("")
    logger.info("Using embedding model: %s", embed_model_id)
    logger.info("")

    embed_model = OCIGenAIEmbeddings(
        auth_type="API_KEY",
        model_id=embed_model_id,
        service_endpoint=embed_model_endpoint,
        compartment_id=COMPARTMENT_OCID,
    )

    return embed_model


def get_list_collections():
    """
    return the list of available collections in the DB
    """
    with get_db_connection() as conn:
        list_collections = OracleVS4DBLoading.list_collections(conn)

    return list_collections


def get_books(collection_name):
    """
    return the list of books in collection
    """
    with get_db_connection() as conn:
        list_books_in_collection = OracleVS4DBLoading.list_books_in_collection(
            connection=conn, collection_name=collection_name
        )

    return list_books_in_collection


def delete_documents_in_collection(collection_name, doc_names):
    """
    drop documents in the given collection
    """
    if len(doc_names) > 0:
        with get_db_connection() as conn:
            logger.info("Delete docs: %s in collection %s", doc_names, collection_name)
            OracleVS4DBLoading.delete_documents(conn, collection_name, doc_names)


def manage_collection(docs, embed_model, collection_name, is_new_collection):
    """
    Create or update a collection in the vector store.
    """
    with get_db_connection() as conn:
        if is_new_collection:
            logger.info(
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
            logger.info(
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
        logger.info("Operation completed for collection: %s", collection_name)
