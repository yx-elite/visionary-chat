import os
from .json_handler import JSONHandler
from .logger import Logger


__all__ = [
    'JSONHandler',
    'Logger'
]

# Get the package name based on the directory name
package_name = os.path.basename(os.path.dirname(__file__))

# Initialize the logger instance
log = Logger(logger_name=package_name, log_level='info')
logger = log.get_logger()

logger.info('Module initialization complete.')