"""
Factory for the Vector Store based on 23AI
"""

import oracledb
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.embeddings import OCIGenAIEmbeddings
from langchain_community.vectorstores.oraclevs import OracleVS

from config_reader import ConfigReader
from config_private import (
    COMPARTMENT_OCID,
    CONNECT_ARGS,
)

from utils import get_console_logger

config = ConfigReader("config.toml")


def create_embedding_model():
    """
    Create the Embedding Model
    """
    embed_model_id = config.find_key("embed_model_id")
    embed_model_endpoint = config.find_key("embed_model_endpoint")

    embed_model = OCIGenAIEmbeddings(
        auth_type="API_KEY",
        model_id=embed_model_id,
        service_endpoint=embed_model_endpoint,
        compartment_id=COMPARTMENT_OCID,
    )

    return embed_model


def create_db_connection():
    """
    Create the DB Connection
    """
    conn = oracledb.connect(**CONNECT_ARGS)

    return conn


def create_vector_store(collection_name: str):
    """
    Create the Vector Store
    """
    logger = get_console_logger()

    v_store = None

    try:
        embed_model = create_embedding_model()
        connection = create_db_connection()

        v_store = OracleVS(
            client=connection,
            table_name=collection_name,
            distance_strategy=DistanceStrategy.COSINE,
            embedding_function=embed_model,
        )
    except oracledb.Error as e:
        err_msg = "An error occurred in get_vector_store: " + str(e)

        logger.error(err_msg)

    return v_store
