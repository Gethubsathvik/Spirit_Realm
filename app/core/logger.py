import logging
import os
from app.config import Config

def setup_logger(name):
    """Set up and return a configured logger."""
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if the logger already exists
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # File handler
        try:
            file_handler = logging.FileHandler(Config.LOG_FILE)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not set up file logger: {e}")
            
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger
