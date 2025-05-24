import mysql.connector
from mysql.connector import Error
import os
from src.shared.infraestructure.logger import get_logger
from dotenv import load_dotenv


logger = get_logger(__name__)

load_dotenv()

config = {
    'host': os.getenv("MYSQL_TEST_DB_HOST"),
    'user': os.getenv("MYSQL_TEST_DB_USER"),
    'password': os.getenv("MYSQL_TEST_DB_PASSWORD"),
    'database': os.getenv("MYSQL_TEST_DB_NAME"),
    'port': os.getenv("MYSQL_TEST_DB_PORT")
}

class DatabaseConnection:
    """
    DatabaseConnection provides methods to manage MySQL database connections.
    Attributes:
        config (dict): Configuration parameters for the MySQL connection.
    Methods:
        get_connection():
            Establishes and returns a new MySQL database connection using the provided configuration.
            Raises an exception if the connection fails.
        close_connection(connection):
            Closes the given MySQL database connection if it is currently open.
    """
    def __init__(self):
        self.config = config

    def get_connection(self):
        try:
            connection = mysql.connector.connect(**self.config)
            return connection
        except Error as e:
            logger.error(f"Error al conectar a MySQL: {e}")
            raise e

    def close_connection(self, connection):
        if connection.is_connected():
            connection.close()