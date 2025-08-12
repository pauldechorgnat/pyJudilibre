import pytest
from pyjudilibre import JudilibreClient
from pyjudilibre.exceptions import (
    JudilibreDecisionNotFoundError,
    JudilibreWrongCredentialsError,
    JudilibreWrongURLError,
)

from .config import DECISION_CC_ID, JUDILIBRE_API_KEY, JUDILIBRE_API_URL


def test_get():
    decision_id = DECISION_CC_ID

    client = JudilibreClient(
        judilibre_api_url=JUDILIBRE_API_URL,
        judilibre_api_key=JUDILIBRE_API_KEY,
    )

    decision = client.decision(decision_id=decision_id)

    assert decision.id == decision_id


def test_get_wrong_id():
    decision_id = "obvisously_wrong_id"

    client = JudilibreClient(
        judilibre_api_url=JUDILIBRE_API_URL,
        judilibre_api_key=JUDILIBRE_API_KEY,
    )

    with pytest.raises(JudilibreDecisionNotFoundError):
        client.decision(decision_id=decision_id)


def test_get_wrong_url():
    decision_id = "5fca56cd0a790c1ec36ddc07"

    client = JudilibreClient(
        judilibre_api_url="https://wrong_url.judilibre.com",
        judilibre_api_key=JUDILIBRE_API_KEY,
    )

    with pytest.raises(JudilibreWrongURLError):
        client.decision(decision_id=decision_id)


def test_get_wrong_credentials():
    decision_id = "5fca56cd0a790c1ec36ddc07"

    client = JudilibreClient(
        judilibre_api_url=JUDILIBRE_API_URL,
        judilibre_api_key="obviously_wrong_credentials",
    )

    with pytest.raises(JudilibreWrongCredentialsError):
        client.decision(decision_id=decision_id)
