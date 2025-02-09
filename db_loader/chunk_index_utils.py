"""
chunk index utils

This version is based on docling
"""

import os
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from langchain.docstore.document import Document
from transformers import AutoTokenizer
from config_reader import ConfigReader
from utils import get_console_logger


# TODO: handle tokenizer_name
logger = get_console_logger()
config = ConfigReader("config.toml")

def get_page_num(_chunk):
    """
    try to get the page num (doesn't work for docx)
    """
    try:
        page_num = _chunk.meta.doc_items[0].prov[0].page_no
    except:
        page_num = ""

    return page_num


def load_book_and_split(books_dir, book_name, max_tokens):
    """
    read a book, split in chunks using docling
    """
    # to remove warning
    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    lc_docs = []

    full_name = os.path.join(books_dir, book_name)

    logger.info("Docling converting: %s", book_name)
    converter = DocumentConverter()
    doc = converter.convert(source=full_name).document

    # the tokenizer
    tokenizer_model = config.find_key("tokenizer_model")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_model)

    logger.info("Chunking...")
    hybrid_chunker = HybridChunker(max_tokens=max_tokens, merge_peers=True,
                                   tokenizer=tokenizer)
    
    chunk_iter = hybrid_chunker.chunk(dl_doc=doc)
    chunks = list(chunk_iter)

    logger.info("Creating serialized chunks...")

    for chunk in chunks:
        enriched_text = hybrid_chunker.serialize(chunk=chunk)

        metadata = {"source": book_name, "page": get_page_num(chunk)}
        lc_doc = Document(page_content=enriched_text, metadata=metadata)
        lc_docs.append(lc_doc)

    logger.info("")

    logger.info("Loaded %s chunks...", len(lc_docs))

    return lc_docs
