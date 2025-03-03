# AI Agents Design Patterns
In this folder we want to provide sample implementations for the various Agentic Design Patterns

* **Router**
* **Parallel Flow**
* **Orchestrator**
* **Prompt Chain**

For each pattern we provide an example and suggestions for the implementation
in a dedicated directory,

## Agents based on LangGraph
All the implementation discussed here are based on Langchain, LangGraph and Oracle OCI Generative AI Services.
Most of the implementations are based on Llama 3.3 70B

## Base Node
In **LangGraph** a node can be implemented using:
* a Python function
* A Python class implementing LangChain Runnable

For several reasons I think that, especially when implementing complex workflows, it is better to use a Python class.

One of the reason is that using a Python class I can easily integrate the Agent with an Application Performance Monitoring Service (APM). 

In the examples I provide I have added the code to integrate with OCI APM.

Using the provided [BaseAgentNode](./agent_base_node.py) you need simply to subclass and implement the **_run_impl** method.

## Integration with OCI APM and Observability
More details on how to configure the integration with OCI APM are in a dedicated section.


