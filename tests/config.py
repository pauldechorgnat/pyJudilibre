import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ.get("API_URL")
API_KEY_ID = os.environ.get("API_KEY_ID")

if (API_URL is None) or (API_KEY_ID is None):
    raise ValueError("API_URL and API_KEY_ID should be set")
