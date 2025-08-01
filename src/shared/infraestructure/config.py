import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from src.shared.infraestructure.logger import get_logger

logger = get_logger(__name__)

class ConfigurationError(Exception):
    """Exception raised for configuration-related errors"""
    pass

class Config:
    """
    Centralized configuration management with validation and type conversion.
    """
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            env_file: Optional path to environment file. If None, looks for .env in current directory.
        """
        load_dotenv(env_file)
        self._config = {}
        self._load_configuration()
        self._validate_required_config()
    
    def _load_configuration(self):
        """Load all configuration from environment variables"""
        self._config = {
            # Database Configuration
            'database': {
                'host': os.getenv('MYSQL_TEST_DB_HOST', 'localhost'),
                'user': os.getenv('MYSQL_TEST_DB_USER', ''),
                'password': os.getenv('MYSQL_TEST_DB_PASSWORD', ''),
                'database': os.getenv('MYSQL_TEST_DB_NAME', ''),
                'port': int(os.getenv('MYSQL_TEST_DB_PORT', 3306)),
                'pool_size': int(os.getenv('DB_POOL_SIZE', 5)),
                'pool_name': os.getenv('DB_POOL_NAME', 'mysql_pool'),
            },
            
            # Server Configuration
            'server': {
                'host': os.getenv('SERVER_HOST', 'localhost'),
                'port': int(os.getenv('SERVER_PORT', 8000)),
                'debug': os.getenv('DEBUG', 'false').lower() == 'true',
            },
            
            # Queries
            'queries': {
                'base_property': os.getenv('MYSQL_QUERY_BASE_PROPERTY', ''),
            },
            
            # Logging
            'logging': {
                'level': os.getenv('LOG_LEVEL', 'INFO'),
                'file_path': os.getenv('LOG_FILE_PATH', 'logs/app.log'),
            }
        }
    
    def _validate_required_config(self):
        """Validate that required configuration is present"""
        required_fields = [
            ('queries.base_property', self._config['queries']['base_property']),
        ]
        
        missing_fields = []
        for field_name, value in required_fields:
            if not value:
                missing_fields.append(field_name)
        
        if missing_fields:
            raise ConfigurationError(f"Missing required configuration: {', '.join(missing_fields)}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.
        
        Args:
            key: Configuration key in dot notation (e.g., 'database.host')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration for connection"""
        return self._config['database'].copy()
    
    def get_server_config(self) -> Dict[str, Any]:
        """Get server configuration"""
        return self._config['server'].copy()
    
    def is_debug(self) -> bool:
        """Check if debug mode is enabled"""
        return self.get('server.debug', False)


# Global configuration instance
config = Config()