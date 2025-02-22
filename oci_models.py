"""
Factory for OCI GenAI models
"""

from langchain_community.chat_models import ChatOCIGenAI
from config_reader import ConfigReader
from config_private import COMPARTMENT_OCID

config_reader = ConfigReader("config.toml")

# general LLM
LLM_MODEL_ID = config_reader.find_key("llm_model_id")
LLM_ENDPOINT = config_reader.find_key("llm_model_endpoint")

# we're using command-r-plus model for routing
ROUTER_MODEL_ID = config_reader.find_key("router_model_id")
ROUTER_ENDPOINT = config_reader.find_key("router_model_endpoint")

CUSTOM_RAG_MODEL_ID = config_reader.find_key("custom_rag_model_id")
CUSTOM_RAG_ENDPOINT = config_reader.find_key("custom_rag_model_endpoint")

AD_MODEL_ID = config_reader.find_key("ad_model_id")
AD_ENDPOINT = config_reader.find_key("ad_model_endpoint")


def create_model(model_id=LLM_MODEL_ID, temperature=0.1, max_tokens=1024):
    """
    Create OCI Model for general task
    """
    llm = ChatOCIGenAI(
        model_id=model_id,
        compartment_id=COMPARTMENT_OCID,
        service_endpoint=LLM_ENDPOINT,
        model_kwargs={"temperature": temperature, "max_tokens": max_tokens},
    )
    return llm


def create_model_for_routing(temperature=0, max_tokens=512):
    """
    Create the OCI Model for routing
    """
    llm = ChatOCIGenAI(
        model_id=ROUTER_MODEL_ID,
        compartment_id=COMPARTMENT_OCID,
        service_endpoint=ROUTER_ENDPOINT,
        # for the router we need deterministic output (temp=0)
        # and we don't need many tokens for output (max_tokens=512)
        model_kwargs={"temperature": temperature, "max_tokens": max_tokens},
    )
    return llm


def create_model_for_custom_rag(temperature=0.1, max_tokens=1024):
    """
    Create the OCI Model for custom rag
    """
    llm = ChatOCIGenAI(
        model_id=CUSTOM_RAG_MODEL_ID,
        compartment_id=COMPARTMENT_OCID,
        service_endpoint=CUSTOM_RAG_ENDPOINT,
        model_kwargs={"temperature": temperature, "max_tokens": max_tokens},
    )
    return llm


def create_model_for_answer_directly(temperature=0.1, max_tokens=2048):
    """
    Create the OCI Model for answering directly (no RAG)
    """
    llm = ChatOCIGenAI(
        model_id=AD_MODEL_ID,
        compartment_id=COMPARTMENT_OCID,
        service_endpoint=AD_ENDPOINT,
        model_kwargs={"temperature": temperature, "max_tokens": max_tokens},
    )
    return llm
