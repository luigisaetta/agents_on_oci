"""
Functions for the Document Analyzer
"""

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from oci_models import create_model_for_answer_directly
from notification_queue import send_notification
from utils import get_console_logger

logger = get_console_logger()

# here we create the LLM. A single LLM is used
# but, if needed, every tool can use a different LLM.
# Every tool has a dedicated, focused prompt
llm = create_model_for_answer_directly()


# Graph state
class State(TypedDict):
    """
    The state of the workflow
    """

    # user request, in UI not used
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


# utility function
def invoke_llm(task_name: str, request: str):
    """
    Function to handle LLM call
    """
    logger.info("Calling %s...", task_name)

    try:
        msg = llm.invoke(request)
        response = msg.content if msg else "Error: No response from LLM"
    except Exception as e:
        logger.error("%s failed: %s", task_name, e)
        response = "Error: Unable to process request"

    send_notification(f"{task_name} completed!")
    return response


# Nodes/tools
def call_llm_0(state: State):
    """
    Extract the file name and read it

    in the UI version this is not really needed
    because the input is the uploaded file
    """
    logger.info("Calling llm_0...")

    return {}


def call_llm_1(state: State):
    """First LLM call to generate spelling errors list"""
    top_e = 10
    request = f"Identify top {top_e} spelling errors in the following text: {state['file_text']}"

    response = invoke_llm("Check spelling errors", request)

    return {"output1": response}


def call_llm_2(state: State):
    """Second LLM call to analyze clarity"""
    request = f"""Evaluate from the point of view of clarity the following text:
    {state['file_text']}.
    Provide a score ranging from 1 to 10 (10 is best).
    """

    response = invoke_llm("Check clarity", request)

    return {"output2": response}


def call_llm_3(state: State):
    """Third LLM call to analyze goals"""
    request = f"""Evaluate the following text: {state['file_text']}.
    Check that it defines clear and measurable goals.
    Provide a score ranging from 1 to 10 (10 is best).
    """

    response = invoke_llm("Check goals", request)

    return {"output3": response}


def call_llm_4(state: State):
    """Fourth LLM call to summarize"""
    request = f"""Summarize the following text in one page: {state['file_text']}.
    """

    response = invoke_llm("Summarize", request)

    return {"output4": response}


def call_llm_anonymize(state: State):
    """LLM call to anonymize"""
    request = f"""
    Anonymize the following text by replacing:
    - Client/customer names
    - People’s names
    - Emails
    - Language names

    Do NOT anonymize:
    - The document name

    Text to anonymize:
    {state['combined_output']}
    """

    response = invoke_llm("Anonymize", request)

    return {"final_output": response}


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


#
# Here we build the graph
#
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
    parallel_builder.add_node("anonymizer", call_llm_anonymize)
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

    parallel_builder.add_edge("aggregator", "anonymizer")
    parallel_builder.add_edge("anonymizer", END)

    parallel_workflow = parallel_builder.compile()

    return parallel_workflow
