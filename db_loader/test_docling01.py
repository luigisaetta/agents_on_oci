"""
Test01 docling

Note: tested with pdf, docx.
    docx: doen't get the page_num
"""

from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker


def get_doc_name(doc):
    """
    gets the source document name
    """
    return doc.metadata["source"]


def get_page_number(doc):
    """
    gets the page number

    return page num (can be "")
    """

    try:
        page_num = doc.metadata["dl_meta"]["doc_items"][0]["prov"][0]["page_no"]
    except:
        page_num = ""

    return page_num


# FILE_PATH = "google-ai-agents-whitepaper.pdf"
# FILE_PATH = "the-side-effects-of-metformin-a-review.pdf"
FILE_PATH = "my_ai_agents.docx"

hybrid_chunker = HybridChunker(max_tokens=512, merge_peers=True)

loader = DoclingLoader(file_path=FILE_PATH, chunker=hybrid_chunker)

docs = loader.load()

print("Number of splits: ", len(docs))

for d in docs[:20]:
    print("----------------------")
    print("----------------------")
    print("Doc. name: ", get_doc_name(d))
    print("Page num.: ", get_page_number(d))
    # print("Metadata: ", d.metadata)
    print("----------------------")
    print(f"- {d.page_content=}")
