import requests
import logging
from typing import Collection

logger = logging.getLogger(__name__)

def check_urls(urls: Collection[str], timeout: int = 5) -> dict[str, str]:
    """
    Check the status of a Collection of URLs.

    Args:
        urls (Collection[str]): A list of URLs to check.
        timeout (int, optional): The timeout for the HTTP requests in seconds. Defaults to 5.

    Returns:
        dict[str, str]: A dictionary mapping each URL to its status ("OK" or "FAILED").
    """
    logger.info(f"Started checking {len(urls)} URLs with the timeout of {timeout} seconds.")
    results = {}

    for url in urls:
        status = "UNKNOWN"

        try:
            logger.debug(f"Checking URL: {url}")
            response = requests.get(url, timeout=timeout)

            if response.ok:
                status = f"{response.status_code} OK"
            else:
                status = f"{response.status_code} {response.reason}"
        except requests.exceptions.Timeout:
            status = "TIMEOUT"
            logger.warning("request TimedOut.")
        except requests.exceptions.ConnectionError:
            status = "CONNECTION_ERROR"
            logger.warning("Connection Error")
        except requests.exceptions.RequestException as e:
            status = f"REQUEST_ERROR: {type(e).__name__}"
            logger.error(f"An uunexpected error occured: {e}", exc_info=True)

        results[url] = status
        logger.debug(f"Completed checking: {url:<40} -> {status}")

    logger.info("URL Check finished")
    return results