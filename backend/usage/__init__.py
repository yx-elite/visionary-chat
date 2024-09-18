import os
from .model_info import retrieve_model_info, calculate_model_pricing
from utils.logger import Logger

__all__ = [
    'retrieve_model_info',
    'calculate_model_pricing'
]

# Get the package name based on the directory name
package_name = os.path.basename(os.path.dirname(__file__))

# Initialize the logger instance
log = Logger(logger_name=package_name, log_level='info')
logger = log.get_logger()

logger.info('Module initialization complete.')