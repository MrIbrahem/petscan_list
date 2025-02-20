#!/usr/bin/python3
"""
PetScan API Client Module
"""

import sys
import logging
import urllib.parse
from typing import Dict, List, Union
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_PARAMS = {
    "format": "json",
    "output_limit" : 3000
}
# "combination": "union", "common_wiki": "cats", "depth": "0",

PETSCAN_URL = "https://petscan.wmflabs.org/"


def encode_title(title: str) -> str:
    """URL-encode page titles with special handling for specific characters."""
    # Handle en-dash specifically if needed
    return urllib.parse.quote(title.replace(" ", "_"), safe=":")


def CheckParams(params: Dict[str, str]) -> str:
    # ---
    output_limit = params.get("output_limit", "0")
    # ---
    if str(output_limit).isdigit():
        output_limit = int(output_limit)
        if output_limit < 3000:
            return params
    # ---
    params["output_limit"] = 3000
    # ---
    return params


def build_petscan_url(params: Dict[str, str]) -> str:
    """Construct PetScan API URL with parameters."""
    base_params = {**DEFAULT_PARAMS, **params}
    # ---
    base_params = CheckParams(base_params)
    # ---
    query_string = urllib.parse.urlencode({k: v for k, v in base_params.items() if v is not None}, doseq=True)
    return f"{PETSCAN_URL}?doit=Do_it&{query_string}"


def fetch_petscan_data(params: Dict[str, str]) -> Union[Dict, List]:
    """Fetch and process data from PetScan API."""
    url = build_petscan_url(params)

    if "printurl" in sys.argv:
        logger.info("Generated PetScan URL: %s", url)

    try:
        response = requests.get(url, timeout=25)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", str(e))
        return {}


def process_petscan_results(data: Dict, split_by_ns: False) -> Dict[str, Dict]:
    """Process raw PetScan results into structured data."""
    results = {}

    if not data or "*" not in data or not data["*"]:
        return results
    # print(data)
    for item in data["*"][0]["a"]["*"]:
        # ns = str(item.get("namespace", ""))
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


def get_petscan_results(params: Dict[str, str], split_by_ns: bool = False) -> Union[Dict, List]:
    """Main function to get PetScan results."""
    raw_data = fetch_petscan_data(params)

    if not raw_data:
        return {}

    processed = process_petscan_results(raw_data, split_by_ns=split_by_ns)
    return processed


# Example usage
if __name__ == "__main__":
    params = {"categories": "Arabic literature", "ns": 0, "language": "ar"}

    results = get_petscan_results(params)
    print(f"Found {len(results)} results:")
    for title, data in results.items():
        print(f"- {title} (QID: {data['Q']}, Length: {data['len']})")
