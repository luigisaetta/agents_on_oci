# AI Agents on OCI
This repo will contain a set of **building blocks** and **examples** 
to build **Agentic AI** solutions using Python, **OCI** and Open Source

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

## Motivation
As part of my role, I frequently design and develop prototypes to demonstrate the application of Oracle Cloud Infrastructure (OCI) Generative AI Service and OCI AI Agents in crafting solutions tailored to our partners' and customers' requirements.

To expedite the assembly of these prototypes and any requested demonstrations, I have curated **a collection of fundamental building blocks** and **examples**.

I am now pleased to share these resources with you.

## List of basic building blocks
* A reader for the configuration settings (TOML format)
* A **Router** (based on Cohere Command-r-plus)
* OCI AI **RAG Agent** client
* **SQL Agent** (based on SelectAI) client
* A **custom RAG agent**, based on Langchain, OCI and 23AI
* A Document **Summarizer**
* A component to help **anonymize** documents
* Utility to load documents in DB 23AI (db_loader)

## Examples
* [Test OCI AI RAG Agent](./test_oci_rag_agent.py)
* [Test SQL Agent](./test_select_ai_sql_agent.ipynb)
* [Agent with LangGraph and routing](./langgraph_with_routing.ipynb)
* [Agent for Document Analysis](./doc_analyzer.ipynb)
* [Basic chatbot with memory](./basic_chatbot.ipynb)

## Best practices
Well, even if you're doing wonderful AI, it doesn't mean that you should forget that to be reusable, you should
provide good Python code, well formatted and checked.

These are **my mandatory** best practices:
* use **black** to check and fix formatting
* use **pylint**

These tools are run on the entire codebase, before any commit.

In addition, components must be simple to use. They encapsulate any needed complexity, but to use them you need a few lines of code.
See, for example: [Test SQL Agent](./test_select_ai_sql_agent.ipynb)

## Configurations
All the settings needed, that can be exposed (not private) are managed in a [toml](./config.toml) file. 

In the example provided you find all the configuration needed, for all components and examples.

Obviously:
1. You need to change the settings accordingly to your needs
2. You can remove some of the settings, if you don't need all of them

## Running environment and security
All the examples are designed in a way that enables you to run on your laptop (in my case, my **MacBook**). 
Therefore, you need to have API_KEYS in the right place ($HOME/.config).

Everything can be easily changed to use Instance Principals or Resource Principals, but.. it is up to you. Here, we concentrate on AI.

## Useful references
Well, it is not a best practice to redo again what was already done by someone else, so here I'll point to useful and good documentation.

[RAG Agent] If you need a reference to setup the **OCI AI RAG Agent**, based on 23 AI, [here](https://snicholspa.github.io/tips_tricks_howtos/oci_genai_service/genai_agents_vector_kb/#Task1:CreateOCIPoliciestoAccessOCIGenAIAgents) you can find a good one.

## Project Status
* (06/02/2025) Project has just started
* (07/02/2025) Published first components and examples on Github
* Added document analyzer, with parallel workflow

therefore, it is wip.




