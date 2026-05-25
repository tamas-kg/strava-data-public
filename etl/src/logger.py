import logging
import sys
import json
from pythonjsonlogger.json import JsonFormatter

def setup_logger(name: str, level=logging.INFO):
    """Setup a JSON logger for structured logging"""
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    logHandler = logging.StreamHandler(sys.stdout)
    formatter = JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s'
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    
    return logger