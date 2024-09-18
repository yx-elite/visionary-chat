import os, requests
import streamlit as st
from typing import Optional, Dict, Any
from requests import RequestException
from utils import Logger, JSONHandler


# Initialize logging
module_name = os.path.basename(__file__).split('.')[0]
log = Logger(logger_name=module_name, log_level='info')
logger = log.get_logger()

# API Endpoint
AIGC_PRICING_ENDPOINT = 'https://aigc.x-see.cn/api/pricing'

@st.cache_resource
def retrieve_model_info(base_url: str = AIGC_PRICING_ENDPOINT) -> Optional[Dict[str, Any]]:
    """
    Retrieves model information from the given API endpoint.

    Args:
        base_url (str, optional): The URL of the API endpoint. Defaults to AIGC_PRICING_ENDPOINT.

    Returns:
        Optional[Dict[str, Any]]: The JSON response as a dictionary if successful, or None in case of an error.
    
    """
    logger.debug("Retrieving model info...")
    payload = {}
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.get(base_url, headers=headers, data=payload)
        response.raise_for_status()
        logger.info("Model info retrieved successfully!")
        return response.json()
    except RequestException as e:
        logger.error(f"Request error occurred: {e}")
        return None

def calculate_price(selected_model: str, input_token: int, output_token: int, **kwargs: Any) -> float:
    """
    Calculate the price based on the selected model, input tokens, and output tokens.

    Args:
        selected_model (str): The model for which pricing is to be calculated.
        input_token (int): The number of input tokens used.
        output_token (int): The number of output tokens generated.
        **kwargs: Additional optional parameters
            - category_rate (float): The rate applied to the model's token calculation. Defaults to 0.49.
            - model_infos (dict): Information about different models. Defaults to backup_path

    Returns:
        float: The calculated price, or 0 if the model information is invalid.
    
    """
    backup_path = '../backup/model_info.json'
    category_rate: float = kwargs.get('category_rate', 0.49)
    model_infos = kwargs.get('model_infos') or JSONHandler.read_json_file(backup_path)
    
    model_infos = model_infos.get('data')
    model_info = next((m for m in model_infos if m.get('model_name') == selected_model), None)
    
    if model_info and model_info.get('quota_type') == 0:   # Token based pricing
            model_ratio: int = model_info.get('model_ratio')
            completion_ratio: int = model_info.get('completion_ratio')
            
            logger.info("Model pricing calculated successfully!")
            return category_rate * model_ratio * (input_token + output_token * completion_ratio) / 500000
    
    logger.warning('Invalid model or pricing type, returning 0 as price.')
    return 0.0


# Example Usage
if __name__ == "__main__":
    data = retrieve_model_info()
    pricing = calculate_price(
        selected_model='gpt-3.5-turbo-instruct',
        input_token=1000,
        output_token=1000,
        category_rate=1.0,   # Main category
        model_infos=data
    )
    print(f"Model Pricing\t: $ {pricing:.4f}")