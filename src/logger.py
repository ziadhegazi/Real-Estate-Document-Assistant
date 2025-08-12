import logging
import os
from  datetime import datetime

# Define the log directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Define the log file path with a daily timestamp
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Configure the logger
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

def get_logger(name: str):
    """
    Returns a logger instance with the specified name.
    
    This allows for module-specific logging.
    """
    return logging.getLogger(name)

# Testing logger.py file /// python src/logger.py
"""
if __name__ == "__main__":
    logger = get_logger(__name__)
    logging.info("Logging has started")
"""