import os
import shutil
import logging
import re
import time
from config import (
    LOG_DIRECTORY,
    PROCESS_LOG_FILE,
    ERROR_LOG_FILE,
)

def setup_logging():
    """Sets up logging for process and error logs prepare directories."""
    os.makedirs(LOG_DIRECTORY, exist_ok=True)

    # Create a timestamp suffix for log files
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    
    process_log_path = os.path.join(LOG_DIRECTORY, f"{timestamp}_{PROCESS_LOG_FILE}")
    error_log_path = os.path.join(LOG_DIRECTORY, f"{timestamp}_{ERROR_LOG_FILE}")

    # Clear logs and delete output folder at the start of each run
    # Just opening in write mode clears the file

    # open(process_log_path, 'w').close()
    # open(error_log_path, 'w').close()
    
    # Configure Error logging
    
    error_logger = logging.getLogger('error_logger')
    error_logger.setLevel(logging.ERROR)
    error_handler = logging.FileHandler(error_log_path)
    error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    error_handler.setFormatter(error_formatter)
    error_logger.addHandler(error_handler)
    
    # Configure Process logging
    process_logger = logging.getLogger('process_logger')
    process_logger.setLevel(logging.INFO)
    process_handler = logging.FileHandler(process_log_path)
    process_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    process_handler.setFormatter(process_formatter)
    process_logger.addHandler(process_handler)

    return process_logger, error_logger


