"""
Functions for doc analyzer
"""

import re
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
import pdfplumber

from oci_models import create_model_for_answer_directly
from utils import get_console_logger

logger = get_console_logger()

# here we create the LLM. A single LLM is used
# but, if needed, every tool can use a different LLM.
# Every tool has a dedicated, focused prompt
llm = create_model_for_answer_directly()


def read_pdf(file_name):
    """
    read the content of the pdf file
    """
    testo = ""
    with pdfplumber.open(file_name) as pdf:
        for pagina in pdf.pages:
            testo += pagina.extract_text() + "\n"
    return testo


def extract_file_name(text):
    """
    extract the file name
    """
    match = re.search(r"```(.*?)```", text)
    if match:
        return match.group(1)
    return None


# Graph state
class State(TypedDict):
    """
    The state of the workflow
    """

    request: str
    file_name: str
    file_text: str

    # output for single tools
    output1: str
    output2: str
    output3: str
    output4: str
    # output from aggregator
    combined_output: str

    final_output: str


# Nodes
def call_llm_0(state: State):
    """
    Extract the file name and read it

    in the UI version this is not really needed
    """
    logger.info("Calling llm_0...")

    return


def call_llm_1(state: State):
    """First LLM call to generate spelling errors list"""
    top_e = 10

    logger.info("Calling llm_1 to identify spelling errors...")

    request = f"Identify top {top_e} spelling errors in the following text: {state['file_text']}"
    msg = llm.invoke(request)

    return {"output1": msg.content}


def call_llm_2(state: State):
    """Second LLM call to analyze clarity"""

    logger.info("Calling llm_2 to analyze clarity...")

    request = f"""Evaluate from the point of view of clarity the following text:
    {state['file_text']}.
    Provide a score ranging from 1 to 10 (10 is best).
    """

    msg = llm.invoke(request)

    return {"output2": msg.content}


def call_llm_3(state: State):
    """Third LLM call to analyze goals"""

    logger.info("Calling llm_3 to analyze goals...")

    request = f"""Evaluate the following text: {state['file_text']}.
    Check that it defines clear and measurable goals.
    Provide a score ranging from 1 to 10 (10 is best).
    """

    msg = llm.invoke(request)

    return {"output3": msg.content}


def call_llm_4(state: State):
    """Fourth LLM call to summarize"""

    logger.info("Calling llm_4 to summarize...")

    request = f"""Summarize the following text in one page: {state['file_text']}.
    """

    msg = llm.invoke(request)

    return {"output4": msg.content}


def aggregator(state: State):
    """Combine all the outputs from steps into a single output"""

    logger.info("Aggregating outputs...")

    # here we can add whatever logic we want,
    combined = f"## Analysis of the document: {state['file_name']}\n\n"
    combined += f"### Summary:\n{state['output4']}\n\n"
    combined += f"### Clarity:\n{state['output2']}\n\n"
    combined += f"### Goals:\n{state['output3']}\n\n"
    combined += f"### Spelling errors:\n{state['output1']}\n\n"

    return {"combined_output": combined}


def call_llm_anonymize(state: State):
    """LLM call to anonymize"""

    logger.info("Calling llm_anonymize to anonymize text...")

    request = f"""Anonymize the following text replacing client/customer name, people names, emails.
    Don't anonymize: the document name.
    Text: {state['combined_output']}.
    """

    msg = llm.invoke(request)

    return {"final_output": msg.content}


def build_workflow():
    """
    Build the workflow
    """
    # Build workflow
    parallel_builder = StateGraph(State)

    # Add nodes
    parallel_builder.add_node("call_llm_0", call_llm_0)
    parallel_builder.add_node("call_llm_1", call_llm_1)
    parallel_builder.add_node("call_llm_2", call_llm_2)
    parallel_builder.add_node("call_llm_3", call_llm_3)
    parallel_builder.add_node("call_llm_4", call_llm_4)
    parallel_builder.add_node("call_llm_anonymize", call_llm_anonymize)
    parallel_builder.add_node("aggregator", aggregator)

    # Add edges to connect nodes
    parallel_builder.add_edge(START, "call_llm_0")

    # parallel calls to work on different focused tasks
    parallel_builder.add_edge("call_llm_0", "call_llm_1")
    parallel_builder.add_edge("call_llm_0", "call_llm_2")
    parallel_builder.add_edge("call_llm_0", "call_llm_3")
    parallel_builder.add_edge("call_llm_0", "call_llm_4")

    # to aggregator
    parallel_builder.add_edge("call_llm_1", "aggregator")
    parallel_builder.add_edge("call_llm_2", "aggregator")
    parallel_builder.add_edge("call_llm_3", "aggregator")
    parallel_builder.add_edge("call_llm_4", "aggregator")

    parallel_builder.add_edge("aggregator", "call_llm_anonymize")
    parallel_builder.add_edge("call_llm_anonymize", END)

    parallel_workflow = parallel_builder.compile()

    return parallel_workflow
