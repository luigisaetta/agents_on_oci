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
    output5: str

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
def call_llm_0(state: State) -> dict:
    """
    Extract the file name and read it

    in the UI version this is not really needed
    because the input is the uploaded file
    """
    logger.info("Calling llm_0...")

    return {}


def call_llm_1(state: State) -> dict:
    """First LLM call to generate spelling errors list"""
    top_e = 10
    request = f"""
    You are an expert proofreader with a keen eye for spelling accuracy. 
    Your task is to identify and analyze the most frequent or impactful spelling errors in the provided text.

    ### Instructions:
    1. Identify the **top {top_e} most frequent or impactful spelling errors**.
    2. List each error along with its **corrected form**.
    3. If possible, explain any recurring spelling patterns or common mistakes found in the text.
    4. Provide a **spelling accuracy score** from **1 to 10**, where:
    - **10** means "no spelling errors detected."
    - **1** means "severe spelling issues throughout the text."

    ### Text for Analysis:
    {state['file_text']}

    ### Expected Response Format:
    **Top {top_e} Spelling Errors:**
    1. ...
    2. ...
    ...
    
    **Spelling Accuracy Score:** X/10  
    **Observations:** [Brief analysis of error patterns, if applicable]  
    """

    response = invoke_llm("Check spelling errors", request)

    return {"output1": response}


def call_llm_2(state: State) -> dict:
    """Second LLM call to analyze clarity"""
    request = f"""
    You are an expert document reviewer with a strong focus on clarity and readability. 
    Your task is to evaluate the following text based on clarity, coherence, and ease of understanding.

    ### Evaluation Criteria:
    1. **Clarity**: Is the text straightforward and free of ambiguity?
    2. **Coherence**: Does the text flow logically from one idea to the next?
    3. **Conciseness**: Is the information presented in a precise and to-the-point manner?
    4. **Readability**: Would an average reader easily comprehend the content?

    ### Instructions:
    - Provide a clarity score from **1 to 10**, where **10** means "extremely clear" and **1** means "very unclear."
    - Briefly **justify** your rating in 2-3 sentences.
    - If the text has major issues, suggest **suggest specific improvements in a bullet-point list**.

    ### Text for Evaluation:
    {state['file_text']}

    ### Expected Response Format:
    **Clarity Score:** X/10  
    **Justification:** [1-2 sentence explanation]  
    **Suggested Improvements (if any):** [Specific ways to enhance clarity]  
    """

    response = invoke_llm("Check clarity", request)

    return {"output2": response}


def call_llm_3(state: State) -> dict:
    """Third LLM call to analyze goals"""
    request = f"""
    You are an expert in goal-setting and document evaluation. 
    Your task is to assess whether the following text clearly defines **specific, measurable, and actionable goals**.

    ### **Evaluation Criteria:**
    1. **Clarity**: Are the goals explicitly stated and easy to understand?
    2. **Measurability**: Can the success of these goals be **quantified or objectively evaluated**?
    3. **Actionability**: Do the goals provide clear steps or strategies for achieving them?
    4. **Relevance**: Are the goals aligned with the overall purpose of the text?

    ### **Instructions:**
    - Provide a **goal clarity score** from **1 to 10**, where:
    - **10** = "Goals are exceptionally clear, measurable, and actionable."
    - **1** = "Goals are vague, missing, or entirely unclear."
    - Justify your rating in **2-3 sentences**.
    - If the goals are unclear or lacking, **suggest specific improvements in a bullet-point list**.

    ### **Text for Evaluation:**
    {state['file_text']}

    ### **Expected Response Format:**
    **Goal Clarity Score:** X/10  
    **Justification:**  
    [2-3 sentence explanation]  

    **Suggested Improvements:**  
    - [First improvement suggestion]  
    - [Second improvement suggestion]  
    - [Third improvement suggestion] (if applicable)  
    """

    response = invoke_llm("Check goals", request)

    return {"output3": response}


def call_llm_4(state: State) -> dict:
    """Fourth LLM call to summarize"""
    request = f"""
    You are an expert summarizer with strong analytical skills. 
    Your task is to generate a **clear, concise, and well-structured** summary of the following text.

    ### **Instructions:**
    - Summarize the text in a way that captures its **main ideas, key points, and essential details**.
    - Keep the summary **within one page** (approximately **250-300 words**).
    - Maintain **logical flow and coherence** in the summary.
    - Preserve the **original intent and meaning** while using **clear and concise language**.
    - Avoid unnecessary details, repetitions, or excessive examples.

    ### **Text to Summarize:**
    {state['file_text']}

    ### **Expected Response Format:**
    **Summary:**  
    [Well-structured and concise summary, approximately 250-300 words]  
    """

    response = invoke_llm("Summarize", request)

    return {"output4": response}


def call_llm_5(state: State) -> dict:
    """Fifth llm call to analyze timelines"""
    request = f"""
    You are an expert in project planning and deadline analysis.  
    Your task is to evaluate the **timelines and deadlines** defined in the following document.

    ### **Evaluation Criteria:**
    1. **Clarity** - Are the timelines clearly stated and easy to follow?
    2. **Realism** - Are the deadlines achievable based on the document's context?
    3. **Consistency** -Do the timelines align with the overall objectives?
    4. **Completeness** - Are key milestones, start dates, and end dates clearly outlined?

    ### **Instructions:**
    - Identify any **gaps, inconsistencies, or unrealistic deadlines**.
    - Provide a **timeline clarity score from 1 to 10**, where:
    - **10** = "Timelines are clear, realistic, and well-structured."
    - **1** = "Timelines are vague, inconsistent, or missing."
    - If improvements are needed, list **specific suggestions in a bullet-point format**.

    ### **Text for Analysis:**
    {state['file_text']}

    ### **Expected Response Format:**
    **Timeline Clarity Score:** X/10  
    **Observations:**  
    [2-3 sentence explanation of findings]  

    **Suggested Improvements:**  
    - [First improvement suggestion]  
    - [Second improvement suggestion]  
    - [Third improvement suggestion] (if applicable)  
    """
    response = invoke_llm("Analyze timelines", request)

    return {"output5": response}


def call_llm_anonymize(state: State) -> dict:
    """LLM call to anonymize"""
    request = f"""
    Anonymize the following text by replacing:
    - Client/customer names
    - Company names (different by Oracle)
    - People’s names
    - Emails
    - Language names

    Do NOT anonymize:
    - The word Oracle
    - The document name

    Text to anonymize:
    {state['combined_output']}
    """

    response = invoke_llm("Anonymize", request)

    return {"final_output": response}


def aggregator(state: State) -> dict:
    """Combine all the outputs from steps into a single output"""

    logger.info("Aggregating outputs...")

    # here we can add whatever logic we want,
    combined = f"## Analysis of the document: {state['file_name']}\n\n"
    combined += f"### Summary:\n{state['output4']}\n\n"
    combined += f"### Clarity:\n{state['output2']}\n\n"
    combined += f"### Goals:\n{state['output3']}\n\n"
    combined += f"### Timelines:\n{state['output5']}\n\n"
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
    parallel_builder.add_node("call_llm_5", call_llm_5)
    parallel_builder.add_node("anonymizer", call_llm_anonymize)
    parallel_builder.add_node("aggregator", aggregator)

    # Add edges to connect nodes
    parallel_builder.add_edge(START, "call_llm_0")

    # parallel calls to work on different focused tasks
    parallel_builder.add_edge("call_llm_0", "call_llm_1")
    parallel_builder.add_edge("call_llm_0", "call_llm_2")
    parallel_builder.add_edge("call_llm_0", "call_llm_3")
    parallel_builder.add_edge("call_llm_0", "call_llm_4")
    parallel_builder.add_edge("call_llm_0", "call_llm_5")

    # to aggregator
    parallel_builder.add_edge("call_llm_1", "aggregator")
    parallel_builder.add_edge("call_llm_2", "aggregator")
    parallel_builder.add_edge("call_llm_3", "aggregator")
    parallel_builder.add_edge("call_llm_4", "aggregator")
    parallel_builder.add_edge("call_llm_5", "aggregator")

    parallel_builder.add_edge("aggregator", "anonymizer")
    parallel_builder.add_edge("anonymizer", END)

    parallel_workflow = parallel_builder.compile()

    return parallel_workflow
