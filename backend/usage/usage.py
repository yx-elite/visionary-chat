import os, requests
from datetime import date
from typing import Optional, Tuple, Dict, Any
from requests import RequestException
from utils import Logger


# Initialize logging
module_name = os.path.basename(__file__).split('.')[0]
log = Logger(logger_name=module_name, log_level='info')
logger = log.get_logger()


def _key_subscription(api_key: str) -> Optional[Dict[str, Any]]:
    """
    Fetches the subscription details for the provided API key.

    Args:
        api_key (str): The API key for authentication.

    Returns:
        Optional[Dict[str, Any]]: Subscription details if successful, None if there is an error.
    
    """
    logger.debug("Fetching API key subscription status...")
    base_url = 'https://aigc.x-see.cn/v1/dashboard/billing/subscription'
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    try:
        response = requests.get(base_url, headers=headers, data=payload)
        response.raise_for_status()
        logger.info("API key subscription retrieved successfully!")
        return response.json()
    except RequestException as e:
        logger.error(f"Request error occurred: {e}")
        raise

def _key_usage(api_key: str, start_date: str='2024-6-6', end_date: str=date.today()) -> Optional[Dict[str, Any]]:
    """
    Fetches the usage details for the provided API key within a specified date range.

    Args:
        api_key (str): The API key for authentication.
        start_date (str, optional): The start date for fetching usage data. Defaults to '2024-6-6'.
        end_date (str, optional): The end date for fetching usage data. Defaults to date.today().

    Returns:
        Optional[Dict[str, Any]]: Usage details if successful, None if there is an error.
    
    """
    logger.debug("Fetching API key usage...")
    base_url = f'https://aigc.x-see.cn/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}'
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    try:
        response = requests.get(base_url, headers=headers, data=payload)
        response.raise_for_status()
        logger.info("API key usage retrieved successfully!")
        return response.json()
    except RequestException as e:
        logger.error(f"Request error occurred: {e}")
        raise

def _key_request_log(api_key: str) -> Optional[Dict[str, Any]]:
    """
    Fetches the request logs for the provided API key.

    Args:
        api_key (str): The API key for authentication.

    Returns:
        Optional[Dict[str, Any]]: Request logs if successful, None if there is an error.
    
    """
    logger.debug("Fetching API key request logs...")
    base_url = f'https://aigc.x-see.cn/api/log/token?key={api_key}'
    payload = {}
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.get(base_url, headers=headers, data=payload)
        response.raise_for_status()
        logger.info("API key request logs retrieved successfully!")
        return response.json()
    except RequestException as e:
        logger.error(f"Request error occurred: {e}")
        raise

def retrieve_key_usage_details(api_key: str) -> Tuple[Optional[Dict], Optional[Dict], Optional[Dict]]:
    """
    Retrieves subscription details, usage data, and request logs for the provided API key.

    Args:
        api_key (str): The API key for authentication.

    Returns:
        Tuple[Optional[Dict], Optional[Dict], Optional[Dict]]: 
            A tuple containing:
            - Subscription details
            - Usage data
            - Request logs
    
    """
    logger.info('Fetching API key details...')
    try:
        return _key_subscription(api_key), _key_usage(api_key), _key_request_log(api_key)
    except Exception as e:
        logger.error(f'An unexpected error has occured: {e}')
        raise


# Example Usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    
    load_dotenv(dotenv_path='./config/.env')
    openai_api_key = os.getenv('AIGC_API_KEY')

    subscription, key_usage, usage_log = retrieve_key_usage_details(
        api_key=openai_api_key
    )
    
    print(subscription)