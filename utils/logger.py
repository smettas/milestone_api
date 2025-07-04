
from datetime import datetime
import logging
import os

def get_logger(logger_name):
    folder = "logs"
    os.makedirs(folder, exist_ok=True)
    
    filename = os.path.join(folder,f"test_log_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log")
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    return logger