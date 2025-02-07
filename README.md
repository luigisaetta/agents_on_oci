# AI Agents on OCI
This repo will contain a set of **building blocks** and **examples** 
to build **Agentic AI** using Python, **OCI** and Open Source

## Motivation
As part of my job, I often have to design and develop prototypes, to show to our partners
and customers how to use Oracle Cloud (OCI) and OCI Generative AI Service and Agents to build
solutions for their requirements.

I decided then to curate a list of basic building blocks and examples, to be able to more rapidly
assemble these prototypes or any other requested demo.

Then, I thought, **why not sharing these things**?

## List of basic building blocks
* A reader for the TOML config
* A **Router** (based on Cohere Command-r-plus)
* OCI AI **RAG Agent** client
* **SQL Agent** (based on SelectAI) client

## Examples
[Test OCI AI RAG Agent](./test_oci_rag_agent.py)

## Configurations
All the settings needed, that can be exposed (not private) are managed in a toml file (config.toml). In the example provided you find all the configuration needed, for all components and examples.

Obviously:
1. You need to change the settings accordingly to your needs
2. You can remove some of the settings, if you don't need all of them

## Running environment and security
All the examples are designed in a way that enables you to run on your laptop (in my case, my **MacBook**). Therefore, you need to have API_KEYS in the right place ($HOME/.config).

Everything can be easily changed to use Instance Principals or Resource Principals, but.. it is up to you. Here, we concentrate on AI.

## Useful references
Well, it is not a best practice to redo again what was already done by someone else, so here I'll point to useful and good documentation.

[RAG Agent] If you need a reference to setup the **OCI AI RAG Agents**, based on 23 AI, [here](https://snicholspa.github.io/tips_tricks_howtos/oci_genai_service/genai_agents_vector_kb/#Task1:CreateOCIPoliciestoAccessOCIGenAIAgents) you can find a good one.




