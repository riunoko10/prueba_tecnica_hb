import threading
from typing import Optional
import mysql.connector
from mysql.connector import Error, pooling
import os
from dotenv import load_dotenv
from src.shared.infraestructure.logger import get_logger
from src.shared.infraestructure.database.connection import DatabaseConnection

load_dotenv()
logger = get_logger(__name__)


class MySQLConnectionPool(DatabaseConnection):
    """
    MySQL connection pool implementation for improved performance and resource management.
    
    Features:
    - Connection pooling to reduce connection overhead
    - Thread-safe operations
    - Automatic connection cleanup
    - Configuration through environment variables
    """
    
    _instance: Optional['MySQLConnectionPool'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'MySQLConnectionPool':
        """Singleton pattern to ensure only one connection pool instance"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._config = {
            'host': os.getenv("MYSQL_TEST_DB_HOST"),
            'user': os.getenv("MYSQL_TEST_DB_USER"),
            'password': os.getenv("MYSQL_TEST_DB_PASSWORD"),
            'database': os.getenv("MYSQL_TEST_DB_NAME"),
            'port': int(os.getenv("MYSQL_TEST_DB_PORT", 3306)),
            'charset': 'utf8mb4',
            'autocommit': True,
            'raise_on_warnings': True
        }
        
        self._pool_config = {
            'pool_name': 'mysql_pool',
            'pool_size': 5,
            'pool_reset_session': True
        }
        
        self._pool = None
        self._initialized = True
        self._create_pool()
    
    def _create_pool(self) -> None:
        """Create the connection pool"""
        try:
            pool_config = {**self._config, **self._pool_config}
            self._pool = pooling.MySQLConnectionPool(**pool_config)
            logger.info("MySQL connection pool created successfully")
        except Error as e:
            logger.error(f"Error creating MySQL connection pool: {e}")
            raise e
    
    def get_connection(self):
        """Get a connection from the pool"""
        try:
            if not self._pool:
                self._create_pool()
            connection = self._pool.get_connection()
            return connection
        except Error as e:
            logger.error(f"Error getting connection from pool: {e}")
            raise e
    
    def close_connection(self, connection) -> None:
        """Return connection to the pool"""
        try:
            if connection and self.is_connected(connection):
                connection.close()  # This returns the connection to the pool
        except Error as e:
            logger.error(f"Error closing connection: {e}")
    
    def is_connected(self, connection) -> bool:
        """Check if connection is active"""
        try:
            return connection and connection.is_connected()
        except (Error, AttributeError):
            return False
    
    def close_pool(self) -> None:
        """Close all connections in the pool"""
        try:
            if self._pool:
                # Note: mysql-connector-python doesn't have a direct close_pool method
                # Connections will be closed when the pool is garbage collected
                self._pool = None
                logger.info("MySQL connection pool closed")
        except Exception as e:
            logger.error(f"Error closing connection pool: {e}")