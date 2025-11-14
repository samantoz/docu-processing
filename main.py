import sys
import file_utils
import time

def main():
    process_logger, error_logger = file_utils.setup_logging()
    process_logger.info(f"Current system time: {time.ctime()}")
    process_logger.info("Logging is set up successfully.")
    process_logger.info("Hello from docling!")
    process_logger.info(f"Python version: {sys.version}")
    process_logger.info(f"Execution path: {sys.executable}")
if __name__ == "__main__":
    main()
