"""
UI for the Dc Analyzer
"""

import streamlit as st
import pdfplumber
from doc_analyzer_backend import build_workflow


def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n\n"
    return text


def stream_output(_iterator):
    """
    Utility to support streaming of output from last node
    """
    # Placeholder for streaming output
    output_placeholder = st.empty()

    accumulated_response = ""
    for message, metadata in _iterator:
        # only the output from the final node
        if metadata.get("langgraph_node") == "anonymizer":
            # Append new content
            accumulated_response += message.content
            # Update the placeholder with the accumulated content
            output_placeholder.markdown(accumulated_response, unsafe_allow_html=True)


# Streamlit UI
st.title("AI Document Analyzer")


# Move file uploader to the sidebar
with st.sidebar:
    st.header("Upload PDF File")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# Process the uploaded file
if uploaded_file is not None:
    extracted_text = extract_text_from_pdf(uploaded_file)
    f_name = uploaded_file.name

    if extracted_text.strip():
        # instantiate the agent
        workflow = build_workflow()

        # inputs to the agent
        inputs = {"file_name": f_name, "file_text": extracted_text}

        # invoke the agent
        _iter = workflow.stream(inputs, stream_mode="messages")

        st.info("Processing file..")

        stream_output(_iter)

    else:
        st.warning(
            "No text could be extracted. The PDF might be scanned or contain images."
        )
else:
    st.info("Upload a PDF file from the sidebar to extract text.")
