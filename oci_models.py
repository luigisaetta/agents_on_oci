"""
Factory for OCI GenAI models
"""

from langchain_community.chat_models import ChatOCIGenAI
from config_reader import ConfigReader
from config_private import COMPARTMENT_OCID

config_reader = ConfigReader("config.toml")

# we're using command-r-plus model for routing
ROUTER_MODEL_ID = config_reader.find_key("router_model_id")
ROUTER_ENDPOINT = config_reader.find_key("router_model_endpoint")

CUSTOM_RAG_MODEL_ID = config_reader.find_key("custom_rag_model_id")
CUSTOM_RAG_ENDPOINT = config_reader.find_key("custom_rag_model_endpoint")

AD_MODEL_ID = config_reader.find_key("ad_model_id")
AD_ENDPOINT = config_reader.find_key("ad_model_endpoint")


def create_model_for_routing():
    """
    Create the OCI Model for routing
    """
    llm = ChatOCIGenAI(
        model_id=ROUTER_MODEL_ID,
        compartment_id=COMPARTMENT_OCID,
        service_endpoint=ROUTER_ENDPOINT,
        # for the router we need deterministic output (temp=0)
        # and we don't need many tokens for output (max_tokens=512)
        model_kwargs={"temperature": 0, "max_tokens": 512},
    )
    return llm


def create_model_for_custom_rag():
    """
    Create the OCI Model for custom rag
    """
    llm = ChatOCIGenAI(
        model_id=CUSTOM_RAG_MODEL_ID,
        compartment_id=COMPARTMENT_OCID,
        service_endpoint=CUSTOM_RAG_ENDPOINT,
        model_kwargs={"temperature": 0.1, "max_tokens": 1024},
    )
    return llm


def create_model_for_answer_directly():
    """
    Create the OCI Model for answering directly
    """
    llm = ChatOCIGenAI(
        model_id=AD_MODEL_ID,
        compartment_id=COMPARTMENT_OCID,
        service_endpoint=AD_ENDPOINT,
        model_kwargs={"temperature": 0.1, "max_tokens": 2024},
    )
    return llm
