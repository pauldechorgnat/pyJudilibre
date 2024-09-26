from pyjudilibre import JudilibreClient
from pyjudilibre.models import SearchResult

from .config import API_KEY_ID, API_URL


def test_search():
    client = JudilibreClient(
        api_url=API_URL,
        api_key_id=API_KEY_ID,
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
        assert isinstance(r, SearchResult)
        assert r.jurisdiction.value == "Cour de cassation"
        assert "accident" in "".join(r.highlights.text).lower(), "".join(r.highlights.text)
        assert "voiture" in "".join(r.highlights.text).lower(), "".join(r.highlights.text)
