import logging
from datetime import datetime

class ControlLog:
    def __init__(self):
        self.log = logging.basicConfig(level=logging.INFO)
    
    def log_info(self, message):
        logging.info(f"{datetime.now()} - {message}")
    
    def log_error(self, message):
        logging.error(f"{datetime.now()} - {message}")

    def log_warning(self, message):
        logging.warning(f"{datetime.now()} - {message}")

    def log_debug(self, message):
        logging.debug(f"{datetime.now()} - {message}")