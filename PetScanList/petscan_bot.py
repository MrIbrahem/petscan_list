
#!/usr/bin/python3
"""
PetScan API Client Module
"""

import sys
import logging
import urllib.parse
from typing import Dict, List, Union
import requests

# Constants
PETSCAN_URL = "https://petscan.wmflabs.org/"
OUTPUT_LIMIT = 3000

# Configure logging in the main guard
logger = logging.getLogger(__name__)

DEFAULT_PARAMS = {
    "format": "json",
    "output_limit": OUTPUT_LIMIT
}


def encode_title(title: str) -> str:
    """URL-encode page titles with special handling for specific characters."""
    # Handle en-dash specifically if needed
    return urllib.parse.quote(title.replace(" ", "_"), safe=":")


def validate_and_sanitize_params(params: Dict[str, Union[str, int]]) -> Dict[str, Union[str, int]]:
    """Validate and sanitize the parameters."""
    output_limit = params.get("output_limit", 0)
    if isinstance(output_limit, str) and output_limit.isdigit():
        output_limit = int(output_limit)

    if output_limit > OUTPUT_LIMIT:
        logger.error("Invalid output_limit: %s", output_limit)
        params["output_limit"] = OUTPUT_LIMIT

    return params


def build_petscan_url(params: Dict[str, Union[str, int]]) -> str:
    """Construct PetScan API URL with parameters."""
    query_string = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}, doseq=True)
    return f"{PETSCAN_URL}?doit=Do_it&{query_string}"


def fetch_petscan_data(params: Dict[str, Union[str, int]]) -> Union[Dict, List]:
    """Fetch and process data from PetScan API."""
    params = {**DEFAULT_PARAMS, **params}
    params = validate_and_sanitize_params(params)
    url = build_petscan_url(params)

    if "printurl" in sys.argv:
        logger.info("Generated PetScan URL: %s", url)

    try:
        response = requests.get(url, timeout=25)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error occurred: %s", str(http_err))
    except requests.exceptions.ConnectionError as conn_err:
        logger.error("Connection error occurred: %s", str(conn_err))
    except requests.exceptions.Timeout as timeout_err:
        logger.error("Timeout error occurred: %s", str(timeout_err))
    except requests.exceptions.RequestException as req_err:
        logger.error("Request error occurred: %s", str(req_err))

    logger.info("No PetScan results")
    logger.info(url)

    return {}


def process_petscan_results(data: Dict, split_by_ns: bool = False) -> Dict[str, Dict]:
    """Process raw PetScan results into structured data."""
    results = {}

    if not data or "*" not in data or not data["*"]:
        return results

    for item in data["*"][0]["a"]["*"]:
        title = item.get("title", "")
        prefix = item.get("nstext", "")

        if split_by_ns:
            if prefix not in results:
                results[prefix] = {}

        full_title = f"{prefix}:{title}" if prefix else title
        full_title = full_title.replace("_", " ").strip()

        item["title"] = full_title
        if split_by_ns:
            results[prefix][full_title] = item
        else:
            results[full_title] = item

    return results


def get_petscan_results(params: Dict[str, Union[str, int]], split_by_ns: bool = False) -> Union[Dict, List]:
    """Main function to get PetScan results."""
    raw_data = fetch_petscan_data(params)

    if not raw_data:
        return {}

    processed = process_petscan_results(raw_data, split_by_ns=split_by_ns)
    return processed


# Example usage in the main guard
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    params = {"categories": "Arabic literature", "ns": 0, "language": "ar"}

    results = get_petscan_results(params)
    print(f"Found {len(results)} results:")
    for title, data in results.items():
        print(f"- {title} (QID: {data['Q']}, Length: {data['len']})")
