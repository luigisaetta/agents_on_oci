"""
Test custom rag agent
"""

from oci_custom_rag_agent import OCICustomRAGagent

# TODO: add handling of the session
rag_agent = OCICustomRAGagent()

question = "What are the side effects of aspirin?"

print(f"Question: {question}\n")
ai_msg = rag_agent.chat(session_id="1234", message=question)

print(ai_msg["answer"])
print("")
