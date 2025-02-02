import json
import logging
from typing import Dict
from pathlib import Path
logger = logging.getLogger(__name__)


def get_translations(lang: str = "ar") -> Dict[str, str]:
    # Load Arabic translations
    try:
        translations_path = Path(__file__).parent.parent / "I18n/ar.json"
        with open(translations_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load translations for {lang}: {e}")
        return {}
