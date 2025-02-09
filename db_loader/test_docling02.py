"""
test_docling02

seems to me that this method works better than te method in test1
"""

import os
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from langchain.docstore.document import Document
from transformers import AutoTokenizer
from config_reader import ConfigReader

config = ConfigReader("config.toml")

def file_list(directory):
    """
    return the file list in dir
    """
    return [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]


def get_page_num(_chunk):
    """
    try to get the page num (doesn't work for docx)
    """
    try:
        page_num = _chunk.meta.doc_items[0].prov[0].page_no
    except:
        page_num = ""

    return page_num


#
# configs
#
MAX_TOKENS = 1024
BOOKS_DIR = "books"
# to remove warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

lc_docs = []

for f_name in ["aifa_aspirina_500_2022.pdf"]: # file_list(BOOKS_DIR):
    full_name = os.path.join(BOOKS_DIR, f_name)

    print("Docling converting: ", f_name)
    converter = DocumentConverter()
    doc = converter.convert(source=full_name).document

    print("Chunking...")
    tokenizer_model = config.find_key("tokenizer_model")
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_model)

    hybrid_chunker = HybridChunker(max_tokens=MAX_TOKENS, merge_peers=True,
                                   tokenizer=tokenizer)
    chunk_iter = hybrid_chunker.chunk(dl_doc=doc)
    chunks = list(chunk_iter)

    print("Creating serialized chunks...")

    for chunk in chunks:
        enriched_text = hybrid_chunker.serialize(chunk=chunk)

        metadata = {"source": f_name, "page": get_page_num(chunk)}
        lc_doc = Document(page_content=enriched_text, metadata=metadata)
        lc_docs.append(lc_doc)


print("Number of splits: ", len(lc_docs))

for d in lc_docs:
    print("----------------------")
    print("----------------------")
    print(d.metadata)
    print("----------------------")
    print(f"- {d.page_content=}")
