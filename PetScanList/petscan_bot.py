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

# Constants
NAMESPACE_MAPPINGS = {
    "category": {"en": "Category", "commons": "Category", "ar": "تصنيف"},
    "template": {"en": "Template", "commons": "Template", "ar": "قالب"},
    "ns_text": {
        "0": "",
        "1": "نقاش",
        "2": "مستخدم",
        "3": "نقاش المستخدم",
        "4": "ويكيبيديا",
        "5": "نقاش ويكيبيديا",
        "6": "ملف",
        "7": "نقاش الملف",
        "10": "قالب",
        "11": "نقاش القالب",
        "12": "مساعدة",
        "13": "نقاش المساعدة",
        "14": "تصنيف",
        "15": "نقاش التصنيف",
        "100": "بوابة",
        "101": "نقاش البوابة",
        "828": "وحدة",
        "829": "نقاش الوحدة",
        "2600": "موضوع",
        "1728": "فعالية",
        "1729": "نقاش الفعالية",
    },
}

DEFAULT_PARAMS = {"combination": "union", "common_wiki": "cats", "depth": "0", "format": "json"}

PETSCAN_URL = "https://petscan.wmflabs.org/"


def encode_title(title: str) -> str:
    """URL-encode page titles with special handling for specific characters."""
    # Handle en-dash specifically if needed
    return urllib.parse.quote(title.replace(" ", "_"), safe=":")


def build_petscan_url(params: Dict[str, str]) -> str:
    """Construct PetScan API URL with parameters."""
    base_params = {**DEFAULT_PARAMS, **params}
    query_string = urllib.parse.urlencode({k: v for k, v in base_params.items() if v is not None}, doseq=True)
    return f"{PETSCAN_URL}?doit=Do_it&{query_string}"


def get_namespace_prefix(ns: str, lang: str = "ar") -> str:
    """Get namespace prefix based on namespace number and language."""
    ns_text = NAMESPACE_MAPPINGS["ns_text"].get(ns, "")

    if ns == "14":
        return NAMESPACE_MAPPINGS["category"].get(lang, "Category")
    if ns == "10":
        return NAMESPACE_MAPPINGS["template"].get(lang, "Template")

    return ns_text if ns_text else ""


def fetch_petscan_data(params: Dict[str, str]) -> Union[Dict, List]:
    """Fetch and process data from PetScan API."""
    url = build_petscan_url(params)

    if "printurl" in sys.argv:
        logger.info("Generated PetScan URL: %s", url)

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", str(e))
        return [] if params.get("return_dict") else {}


def process_petscan_results(data: Dict, lang: str = "ar") -> Dict[str, Dict]:
    """Process raw PetScan results into structured data."""
    results = {}

    if not data or "*" not in data or not data["*"]:
        return results

    for item in data["*"][0]["a"]["*"]:
        ns = str(item.get("namespace", ""))
        title = item.get("title", "")

        prefix = get_namespace_prefix(ns, lang)
        full_title = f"{prefix}:{title}" if prefix else title
        full_title = full_title.replace("_", " ").strip()

        results[full_title] = {"touched": item.get("touched", ""), "Q": item.get("q", ""), "ns": ns, "len": item.get("len", 0), "title": full_title}

    return results


def get_petscan_results(params: Dict[str, str], return_dict: bool = False) -> Union[Dict, List]:
    """Main function to get PetScan results."""
    raw_data = fetch_petscan_data(params)

    if not raw_data:
        return {} if return_dict else []

    processed = process_petscan_results(raw_data, params.get("language", "ar"))
    return processed if return_dict else list(processed.keys())


# Example usage
if __name__ == "__main__":
    params = {"categories": "Arabic literature", "ns": 0, "language": "ar"}

    results = get_petscan_results(params, return_dict=True)
    print(f"Found {len(results)} results:")
    for title, data in results.items():
        print(f"- {title} (QID: {data['Q']}, Length: {data['len']})")
