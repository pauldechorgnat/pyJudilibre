import pytest

from pyjudilibre import JudilibreClient
from pyjudilibre.exceptions import (
    JudilibreWrongCredentialsError,
    JudilibreWrongURLError,
)

from .config import API_KEY_ID, API_URL


def test_healthcheck():
    client = JudilibreClient(
        api_url=API_URL,
        api_key_id=API_KEY_ID,
    )

    health_check = client.healthcheck()
    assert health_check is True


def test_healthcheck_wrong_url():
    client = JudilibreClient(
        api_url="https://wrong_url.judilibre.com",
        api_key_id=API_KEY_ID,
    )

    with pytest.raises(JudilibreWrongURLError):
        client.healthcheck()


def test_healthcheck_wrong_credentials():
    client = JudilibreClient(
        api_url=API_URL,
        api_key_id="obvisouly_wrong_credentials",
    )

    with pytest.raises(JudilibreWrongCredentialsError):
        client.healthcheck()

    with pytest.raises(JudilibreWrongCredentialsError):
        client.healthcheck()
