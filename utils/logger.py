import logging
import os
from datetime import datetime


class Logger:
    # Log level relationship mapping
    # Ref - https://dev.to/luca1iu/using-the-logger-class-in-python-for-effective-logging-4ghc
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }
    
    def __init__(self, logger_name: str = __name__, log_level: str = 'info', log_directory: str = 'logs'):
        """
        Initializes the logger with the specified name and level and directory.
        If no name is provided, the file/package name is used.
        
        Args:
            logger_name (str): The name of the logger (should be module/package name).
            log_level (str): The log level, e.g., 'debug', 'info'.
            log_directory (str): The directory to store the logs output.
        
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(self.level_relations.get(log_level))
        self.log_directory = log_directory
        
        if not self.logger.hasHandlers():
            console_formatter = logging.Formatter(fmt='%(asctime)s | %(levelname)s | %(name)s.%(funcName)s:%(lineno)d - %(message)s')
            file_formatter = logging.Formatter(fmt='%(asctime)s | %(levelname)s | %(name)s.%(funcName)s:%(lineno)d - %(message)s')
            
            # Default console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.level_relations.get(log_level))
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
            
            # Default file handler
            log_filepath = self._generate_log_filepath()
            file_handler = logging.FileHandler(log_filepath)
            file_handler.setLevel(self.level_relations.get(log_level))
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
    
    def _generate_log_filepath(self) -> str:
        """
        Generates a log path with the filename based on the created date and time.
        
        Returns:
            str: The path to the log file.
        
        """
        os.makedirs(self.log_directory, exist_ok=True)
        
        # Format the current date time into filename
        log_filename = datetime.now().strftime(r"log_%Y%m%d-%H%M%S.log")
        log_filepath = os.path.join(self.log_directory, log_filename)
        return log_filepath
    
    def get_logger(self):
        return self.logger


# Example usage
if __name__ == "__main__":
    log = Logger(logger_name='logging_setup', log_level='debug')
    
    # Both methods are allowable for logging
    # logger = log.get_logger()
    # logger.info("This is info message.")
    
    # Log some messages
    log.logger.debug("This is debug message.")
    log.logger.info("This is info message.")
    log.logger.warning("This is warning message.")
    log.logger.error("This is error message.")
    log.logger.critical("This is critical message.")
    
    # logger.info("This is info message.")
    # logger.info("This is info message.")
    # logger.info("This is info message.")
    # logger.info("This is info message.")
    # logger.error("This is error message.")