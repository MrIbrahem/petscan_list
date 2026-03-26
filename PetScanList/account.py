import os
from dotenv import load_dotenv
try:
    load_dotenv()
except Exception:
    pass

username = os.getenv("WIKIPEDIA_BOT_USERNAME", "")
password = os.getenv("WIKIPEDIA_BOT_PASSWORD", "")
