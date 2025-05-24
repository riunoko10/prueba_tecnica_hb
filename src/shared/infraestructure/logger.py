import logging
import sys
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str = "app_logger") -> logging.Logger:
    """
    Configures and returns a logger instance with best practices:
    - Console and rotating file handlers
    - INFO level by default
    - Structured log format with timestamps
    - Creates logs directory and log file if they don't exist
    """
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger  # Prevent adding handlers multiple times

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Ensure logs directory exists
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "app.log")

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating file handler
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger
