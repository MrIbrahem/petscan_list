import requests
import json
import logging
from typing import Dict
from pathlib import Path
logger = logging.getLogger(__name__)


def get_tt_translations(lang: str = "ar") -> Dict[str, str]:
    url = f"https://tools-static.wmflabs.org/tooltranslate/data/petscan-list/{lang}.json"

    try:
        response = requests.get(url, timeout=25)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", str(e))
        return {}


def get_translations(lang: str = "ar") -> Dict[str, str]:

    translations_path = Path(__file__).parent.parent / "I18n"
    try:
        file = translations_path / f"{lang}.json"
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load translations for {lang}: {e}")
        return {}


def make_translations(key: str, lang: str = "ar") -> str:
    translations = get_translations(lang)

    if not translations:
        translations = get_translations("en")

    return translations.get(key, key)
