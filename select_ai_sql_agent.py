"""
SQL agent based on Select AI

Select AI requires setup in the DB.
A very good guide is this one:
    https://snicholspa.github.io/tips_tricks_howtos/autonomous_database/select_ai/

"""

import oracledb

from sql_agent import SQLAgent
from config_reader import ConfigReader
from config_private import DB_USER, DB_PWD, DSN, WALLET_DIR, WALLET_PWD
from utils import get_console_logger

# create the struct from params in config_private
CONNECT_ARGS = {
    "user": DB_USER,
    "password": DB_PWD,
    "dsn": DSN,
    "config_dir": WALLET_DIR,
    "wallet_location": WALLET_DIR,
    "wallet_password": WALLET_PWD,
}

logger = get_console_logger()


class SelectAISQLAgent(SQLAgent):
    """
    Implementation of the SQL Agent based on Select AI
    """

    def __init__(self, config: ConfigReader):
        """
        init
        """
        self.config = config

    def get_db_connection(self):
        """
        get a connection to data DB
        """
        conn = oracledb.connect(**CONNECT_ARGS)

        return conn

    # @TRACER.start_as_current_span("generate_sql")
    def generate_sql(self, nl_request: str) -> str:
        """
        Generate SQL using Select AI
        """
        verbose = self.config.find_key("verbose")
        profile_name = self.config.find_key("profile_name")

        set_profile_sql = f"""BEGIN
            DBMS_CLOUD_AI.SET_PROFILE('{profile_name}'); 
        END;"""

        gen_sql = ""

        logger.info("Generating SQL...")

        with self.get_db_connection() as conn:
            with conn.cursor() as cursor:
                # before, set the SelectAI profile
                cursor.execute(set_profile_sql)

                # select ai instruction to get the sql generated
                showsql_command = f"SELECT AI showsql '{nl_request}'"

                cursor.execute(showsql_command)

                for row in cursor:
                    gen_sql = row[0]
                    break

        if verbose:
            logger.info(gen_sql)

        return gen_sql

    def check_sql(self, sql) -> bool:
        """
        Check if SQL syntax is correct
        """
        try:
            with self.get_db_connection() as conn:
                with conn.cursor() as cursor:
                    # check that the syntax is correct doing explain plan
                    # that doesn't need execution, it is faster
                    explain_sql = f"EXPLAIN PLAN FOR {sql}"
                    cursor.execute(explain_sql)
            return True
        except oracledb.DatabaseError:
            # try with original SQL to handle special cases
            # where explain is not allowed
            try:
                with self.get_db_connection() as conn:
                    logger.info("Trying without explain plan...")
                    with conn.cursor() as cursor:
                        # for special sql not allowing explain plan
                        cursor.execute(sql)
                return True
            except oracledb.DatabaseError as e:
                (error,) = e.args
                logger.error("Database error: %s", error.message)
                logger.error("Invalid SQL: %s", sql)
        except Exception as e:
            logger.error("Unexpected error: %s", e)
        return False

    def execute_sql(self, sql: str) -> list[dict]:
        """
        Execute the provided SQL and return results as a list of dictionaries.

        Args:
            sql (str): SQL query to execute.

        Returns:
            list[dict]: Query results, with each row represented as a dictionary.
        """
        results = []
        if self.check_sql(sql):
            logger.info("SQL validated. Executing...")
            try:
                with self.get_db_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(sql)
                        columns = [col[0] for col in cursor.description]
                        for row in cursor:
                            results.append(dict(zip(columns, row)))

                logger.info("Executed successfully. Rows fetched: %d", len(results))
            except Exception as e:
                logger.error("Error executing SQL: %s", sql)
                logger.error(e)
        else:
            logger.warning("SQL validation failed. Execution skipped.")
        return results
