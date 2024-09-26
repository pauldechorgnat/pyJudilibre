from pyjudilibre import JudilibreClient
from pyjudilibre.models import JudilibreDecision

from .config import API_KEY_ID, API_URL


def test_export():
    client = JudilibreClient(
        api_url=API_URL,
        api_key_id=API_KEY_ID,
    )

    results = client.export(
        max_results=42,
        verbose=False,
    )

    assert len(results) == 42
    for r in results:
        assert isinstance(r, JudilibreDecision)


def test_export_jurisdiction():
    client = JudilibreClient(
        api_url=API_URL,
        api_key_id=API_KEY_ID,
    )

    # CC
    for jurisdiction_short, jurisdiction in {
        "cc": "Cour de cassation",
        "ca": "Cour d'appel",
        "tj": "Tribunal judiciaire",
    }.items():
        results = client.export(
            max_results=42,
            jurisdictions=[jurisdiction_short],
            verbose=False,
        )
        assert len(results) == 42
        for r in results:
            assert isinstance(r, JudilibreDecision)
            assert r.jurisdiction.value == jurisdiction
