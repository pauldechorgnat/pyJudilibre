import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ.get("API_URL")
API_KEY_ID = os.environ.get("API_KEY_ID")

DECISION_CC_ID = "5fca56cd0a790c1ec36ddc07"
DECISION_CA_ID = "649e75f8f84a5e05db33e6af"

if (API_URL is None) or (API_KEY_ID is None):
    raise ValueError("API_URL and API_KEY_ID should be set")
