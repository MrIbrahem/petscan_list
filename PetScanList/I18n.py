import json
from pathlib import Path


def get_translations(lang="ar"):
    # Load Arabic translations
    try:
        with open(Path(__file__).parent.parent / "I18n/ar.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading translations: {str(e)}")
        return {}
