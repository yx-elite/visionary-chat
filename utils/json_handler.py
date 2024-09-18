import os
import json
from typing import List, Dict, Union, Optional
from utils.logger import Logger


# Initialize logging
module_name = os.path.basename(__file__).split('.')[0]
log = Logger(logger_name=module_name, log_level='info')
logger = log.get_logger()

class JSONHandler:
    @staticmethod
    def save_to_json(file_path: str, data: Union[List, Dict]) -> None:
        """
        Saves the given data to a JSON file at the specified path.
        
        Args:
            file_path (str): The path to the JSON file where the data will be saved.
            data (Union[List, Dict]): The data to be saved in JSON format.
            
        """
        try:
            # Convert file path to absolute path
            absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_path))
            directory = os.path.dirname(absolute_path)
            
            # Ensure the directory exists
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            with open(absolute_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            logger.info(f"Data successfully saved to {absolute_path}.")
        
        except IOError as e:
            logger.error(f"IOError saving data to {absolute_path}: {e}")
        except Exception as e:
            logger.error(f"Error saving data to {absolute_path}: {e}")
    
    @staticmethod
    def read_json_file(file_path: str) -> Union[List, Dict, None]:
        """
        Reads data from a JSON file at the specified path.
        
        Args:
            file_path (str): The path to the JSON file to read.
        
        Returns:
            Union[List, Dict, None]: The data read from the JSON file, or None if an error occurs.
        
        """
        try:
            # Convert file_path to an absolute path
            absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_path))
            with open(absolute_path, 'r') as json_file:
                data = json.load(json_file)
            logger.info(f"Data successfully read from {absolute_path}.")
            return data
        
        except IOError as e:
            logger.error(f"IOError reading data from {absolute_path}: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError reading data from {absolute_path}: {e}")
        except Exception as e:
            logger.error(f"Error reading data from {absolute_path}: {e}")
        
        return None
    
    @staticmethod
    def parse_json_string(json_string: str) -> Union[List, Dict, None]:
        """
        Parses a JSON string into a Python dictionary or list.

        Args:
            json_string (str): The JSON string to be parsed.

        Returns:
            Union[List, Dict, None]: Parsed data as a dictionary or list, or None if an error occurs.
        
        """
        try:
            data = json.loads(json_string)
            logger.info("JSON string successfully parsed.")
            return data
        
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON string: {e}")
        
        return None
    
    @staticmethod
    def write_json_string(data: Union[List, Dict]) -> str:
        """
        Converts a Python list or dict to a JSON string.
        
        Args:
            data (Union[List, Dict]): The data to be converted to a JSON string.
        
        Returns:
            str: JSON string representation of the data, or an empty string if an error occurs.
        
        """
        try:
            json_string = json.dumps(data, indent=4)
            logger.info("Data successfully converted to JSON string.")
            return json_string
        
        except TypeError as e:
            logger.error(f"Error converting data to JSON string: {e}")
        
        return ""


# Example Usage
if __name__ == "__main__":
    # Save data to JSON file
    data = {
        "title": "Save to JSON File",
        "content": "Example content"
    }
    JSONHandler.save_to_json('../response/test_save_to_json.json', data)
    
    # Read data from JSON file
    data = JSONHandler.read_json_file('../response/test_save_to_json.json')
    print(data)
    
    # Parse JSON string
    json_string = '{"title": "Parse JSON String", "content": "Example content"}'
    data = JSONHandler.parse_json_string(json_string)
    print(data)
    
    # Convert data to JSON string
    data = {"title": "Save to JSON String","content": "Example content"}
    json_string = JSONHandler.write_json_string(data)
    print(json_string)

