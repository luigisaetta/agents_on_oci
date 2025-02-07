"""
This is the abstract class that defines the protocol for the
SQL agent

we can have different implementations:
    * Select AI
    * my implementation

    each one is a different class
"""

from abc import ABC, abstractmethod


class SQLAgent(ABC):
    """
    Base class to define the protocol for SQL agent
    """

    @abstractmethod
    def get_db_connection(self):
        """
        get a DB connection
        """

    @abstractmethod
    def generate_sql(self, nl_request: str) -> str:
        """
        Generate an SQL query from a natural language request.
        """

    @abstractmethod
    def check_sql(self, sql) -> bool:
        """
        Check that syntax is ok on the target DB
        """

    @abstractmethod
    def execute_sql(self, sql: str) -> list[dict]:
        """
        Execute the given SQL query and return the result as a list of dictionaries.
        """
