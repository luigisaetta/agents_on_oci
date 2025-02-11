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


# Streamlit UI
st.title("AI Doc Analyzer")

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

        with st.spinner():
            # invoke the agent
            state = workflow.invoke({"file_name": f_name, "file_text": extracted_text})

        st.markdown(state["final_output"], unsafe_allow_html=True)
    else:
        st.warning(
            "No text could be extracted. The PDF might be scanned or contain images."
        )
else:
    st.info("Upload a PDF file from the sidebar to extract text.")
