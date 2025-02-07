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

## List of basc building blocks
* A **Router** (based on Cohere Command-r-plus)
* OCI AI **RAG Agent** client
* **SQL Agent** (based on SelectAI) client

## Configurations
All the settings needed, that can be exposed (not private) are managed in a toml file (config.toml). In the example provided you find all the configuration needed, for all components and examples.

Obviously:
1. You need to change the settings accordingly to your needs
2. You can remove some of the settings, if you don't need all of them

## Running environment and security
All the examples are designed in a way that enables you to run on your laptop (in my case, my **MacBook**). Therefore, you need to have API_KEYS in the right place ($HOME/.config).

Everything can be easily changed to use Instance Principals or Resource Principals, but.. it is up to you. Here, we concentrate on AI.


