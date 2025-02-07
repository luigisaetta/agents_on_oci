"""
Test oci_rag_agent
"""

import json
from oci_rag_agent import OCIRAGAgent

from config_reader import ConfigReader
from config_private import AGENT_ID

SHOULD_STREAM = False

config_reader = ConfigReader("config.toml")

ENDPOINT = config_reader.find_key("rag_endpoint")


def print_response(_response):
    """
    Print the response
    """
    if not SHOULD_STREAM:
        print(_response)
    else:
        # manage streaming
        for event in _response.data.events():
            if "message" in json.loads(event.data):
                # print(event.data)
                print(json.loads(event.data)["message"]["content"]["text"])


rag_client = OCIRAGAgent(AGENT_ID, ENDPOINT, should_stream=SHOULD_STREAM)

sess_id = rag_client.create_session()

questions = [
    "Make a detailed and complete list of known side effects of tachipirin",
    "Can it be used on children?",
    "Puoi fare una lista degli effetti collaterali, in italiano?",
]

for question in questions:
    print("Question: ", question)
    print("")

    response = rag_client.chat(sess_id, question)

    print_response(response)
    print("")
    print("")

rag_client.close_session(sess_id)
