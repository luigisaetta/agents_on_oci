"""
Test custom rag agent
"""

from oci_custom_rag_agent import OCICustomRAGagent

rag_agent = OCICustomRAGagent()

SESSION_ID = rag_agent.create_session()

questions = ["What are the side effects of aspirin?", "Can it be given to children?"]

for question in questions:

    print(f"Question: {question}\n")
    ai_msg = rag_agent.chat(session_id=SESSION_ID, message=question)

    print(ai_msg["answer"])
    print("")

rag_agent.close_session(session_id=SESSION_ID)
