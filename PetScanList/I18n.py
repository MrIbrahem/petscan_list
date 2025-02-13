import json
import logging
from typing import Dict
from pathlib import Path
logger = logging.getLogger(__name__)


def get_translations(lang: str = "ar") -> Dict[str, str]:
    translations_path = Path(__file__).parent.parent / "I18n"
    try:
        file = translations_path / f"{lang}.json"
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load translations for {lang}: {e}")
        return {}
    try:
        file = translations_path / "ar.json"
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load translations for {lang}: {e}")
        return {}
