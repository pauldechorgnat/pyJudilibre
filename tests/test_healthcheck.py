import os

from dotenv import load_dotenv

from pyjudilibre import JudilibreClient

load_dotenv()

API_URL = os.environ.get("API_URL")
API_KEY_ID = os.environ.get("API_KEY_ID")


def test_healthcheck():
    client = JudilibreClient(api_url=API_URL, api_key_id=API_KEY_ID)

    health_check = client.healthcheck()
    assert health_check is True
