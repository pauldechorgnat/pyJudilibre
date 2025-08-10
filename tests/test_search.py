from pyjudilibre import JudilibreClient
from pyjudilibre.models import JudilibreSearchResult

from .config import JUDILIBRE_API_KEY, JUDILIBRE_API_URL


def test_search():
    client = JudilibreClient(
        judilibre_api_url=JUDILIBRE_API_URL,
        judilibre_api_key=JUDILIBRE_API_KEY,
    )

    results = client.search(
        query="accident de voiture",
        operator="exact",
        jurisdictions=["cc"],
        max_results=13,
        verbose=False,
    )

    assert len(results) == 13

    for r in results:
        assert isinstance(r, JudilibreSearchResult)
        assert r.jurisdiction.value == "Cour de cassation"
        assert "accident" in "".join(r.highlights.text).lower(), "".join(r.highlights.text)
        assert "voiture" in "".join(r.highlights.text).lower(), "".join(r.highlights.text)
