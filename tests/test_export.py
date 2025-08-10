from pyjudilibre import JudilibreClient
from pyjudilibre.models import JudilibreDecision

from .config import JUDILIBRE_API_KEY, JUDILIBRE_API_URL


def test_export():
    client = JudilibreClient(
        judilibre_api_url=JUDILIBRE_API_URL,
        judilibre_api_key=JUDILIBRE_API_KEY,
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
        judilibre_api_url=JUDILIBRE_API_URL,
        judilibre_api_key=JUDILIBRE_API_KEY,
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
            assert (r.jurisdiction is not None) and (r.jurisdiction.value) == jurisdiction
