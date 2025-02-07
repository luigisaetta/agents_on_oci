"""
Test SelectAI SQL Agent
"""

from select_ai_sql_agent import SelectAISQLAgent
from config_reader import ConfigReader

config = ConfigReader("config.toml")

sql_agent = SelectAISQLAgent(config)

questions = ["List top 5 sales by sales amount"]

for question in questions:
    print("Question: ", question)
    print("")

    response = sql_agent.generate_sql(question)

    print("SQL: ", response)
    print("")
    print("")
