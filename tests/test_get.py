import pytest

from pyjudilibre import JudilibreClient
from pyjudilibre.exceptions import (
    JudilibreDecisionNotFoundError,
    JudilibreWrongCredentialsError,
    JudilibreWrongURLError,
)

from .config import API_KEY_ID, API_URL, DECISION_CC_ID


def test_get():
    decision_id = DECISION_CC_ID

    client = JudilibreClient(api_url=API_URL, api_key_id=API_KEY_ID)

    decision = client.get(decision_id=decision_id)

    assert decision.id == decision_id


def test_get_wrong_id():
    decision_id = "obvisously_wrong_id"

    client = JudilibreClient(api_url=API_URL, api_key_id=API_KEY_ID)

    with pytest.raises(JudilibreDecisionNotFoundError):
        client.get(decision_id=decision_id)


def test_get_wrong_url():
    decision_id = "5fca56cd0a790c1ec36ddc07"

    client = JudilibreClient(
        api_url="https://wrong_url.judilibre.com", api_key_id=API_KEY_ID
    )

    with pytest.raises(JudilibreWrongURLError):
        client.get(decision_id=decision_id)


def test_get_wrong_credentials():
    decision_id = "5fca56cd0a790c1ec36ddc07"

    client = JudilibreClient(api_url=API_URL, api_key_id="obviously_wrong_credentials")

    with pytest.raises(JudilibreWrongCredentialsError):
        client.get(decision_id=decision_id)
