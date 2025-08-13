import logging
import os
from datetime import datetime

def setup_logger():
    logger = logging.getLogger()

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    # Create log directory if not exists
    os.makedirs("logs", exist_ok=True)

    # Generate dynamic log file with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"logs/log_{timestamp}.log"

    file_handler = logging.FileHandler(log_file) # Creates file output
    formatter = logging.Formatter("%(asctime)s — %(levelname)s — %(filename)s — %(funcName)s — %(message)s") # Defines the format of log lines
    file_handler.setFormatter(formatter) # Apply format to the handler

    logger.addHandler(file_handler) # Add the file handler to the logger

    return logger