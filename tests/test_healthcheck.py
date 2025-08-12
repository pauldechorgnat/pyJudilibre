import pytest
from pyjudilibre import JudilibreClient
from pyjudilibre.exceptions import (
    JudilibreWrongCredentialsError,
    JudilibreWrongURLError,
)

from .config import JUDILIBRE_API_KEY, JUDILIBRE_API_URL


def test_healthcheck():
    client = JudilibreClient(
        judilibre_api_url=JUDILIBRE_API_URL,
        judilibre_api_key=JUDILIBRE_API_KEY,
    )

    health_check = client.healthcheck()
    assert health_check is True


def test_healthcheck_wrong_url():
    client = JudilibreClient(
        judilibre_api_url="https://wrong_url.judilibre.com",
        judilibre_api_key=JUDILIBRE_API_KEY,
    )

    with pytest.raises(JudilibreWrongURLError):
        client.healthcheck()


def test_healthcheck_wrong_credentials():
    client = JudilibreClient(
        judilibre_api_url=JUDILIBRE_API_URL,
        judilibre_api_key="obvisouly_wrong_credentials",
    )

    with pytest.raises(JudilibreWrongCredentialsError):
        client.healthcheck()

    with pytest.raises(JudilibreWrongCredentialsError):
        client.healthcheck()
