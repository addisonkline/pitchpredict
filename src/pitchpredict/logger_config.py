"""
pitchpredict/src/logger_config.py
Created by Addison Kline (akline@baseball-analytica.com)
"""
# external imports
import logging
import os
from datetime import datetime

"""
# generate a timestamped log file name
log_filename = f"log_{datetime.now().strftime('%Y%m%d')}.log"
log_filepath = os.path.join(os.getcwd(), f'logs/{log_filename}')

# config for shared logger
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG to capture all levels of logs
    format='%(asctime)s [%(name)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_filepath),
    ]
)

def get_logger(name):
    return logging.getLogger(name)
"""