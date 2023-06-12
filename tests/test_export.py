import pytest

from pyjudilibre import JudilibreClient
from pyjudilibre.exceptions import JudilibreValueError, JudilibreValueWarning

from .config import API_KEY_ID, API_URL


def test_export():
    client = JudilibreClient(api_url=API_URL, api_key_id=API_KEY_ID)

    results = client.export(max_results=42, verbose=False)

    assert len(results) == 42


def test_export_wrong_ca():
    client = JudilibreClient(api_url=API_URL, api_key_id=API_KEY_ID)

    wrong_values = {
        "locations": "wrong_ca",
        "decision_themes": "wrong_theme",
        "decision_types": "wrong_type",
        "solutions": "wrong_solution",
    }

    for key in wrong_values:
        with pytest.raises(JudilibreValueError):
            client.export(
                **{key: [wrong_values[key]], "juridisctions": ["ca"]},
                action_on_check="raise"
            )

        with pytest.warns(JudilibreValueWarning):
            results = client.export(
                **{key: [wrong_values[key]], "juridisctions": ["ca"]},
                action_on_check="warn"
            )

            assert len(results) == 0, results

            results = client.export(
                **{key: [wrong_values[key]], "juridisctions": ["ca"]},
                action_on_check="ignore"
            )

            assert len(results) == 0, results


def test_export_wrong_cc():
    client = JudilibreClient(api_url=API_URL, api_key_id=API_KEY_ID)

    wrong_values = {
        "decision_themes": "wrong_theme",
        "decision_types": "wrong_type",
        "solutions": "wrong_solution",
        "chambers": "wrong_chamber",
        "formations": "wrong_formation",
        "publications": "w",
    }

    for key in wrong_values:
        with pytest.raises(JudilibreValueError):
            client.export(
                **{key: [wrong_values[key]], "juridisctions": ["cc"]},
                action_on_check="raise"
            )

        with pytest.warns(JudilibreValueWarning):
            results = client.export(
                **{key: [wrong_values[key]], "juridisctions": ["cc"]},
                action_on_check="warn"
            )

            assert len(results) == 0, results

            results = client.export(
                **{key: [wrong_values[key]], "juridisctions": ["cc"]},
                action_on_check="ignore"
            )

            assert len(results) == 0, results
