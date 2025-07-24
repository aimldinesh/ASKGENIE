import logging
import os
from datetime import datetime

# Directory to store log files
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Create a log file with the current date
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# Basic logging configuration
logging.basicConfig(
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    level=logging.INFO,  # Default log level
)


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance.

    Args:
        name (str): Name of the logger (typically the module name).

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
