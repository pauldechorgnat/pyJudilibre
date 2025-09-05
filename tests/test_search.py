import datetime

import pytest

from pyjudilibre.enums import JudilibreOperatorEnum, JurisdictionEnum
from pyjudilibre.models import JudilibreSearchResult

from .config import JURISDICTIONS, LOCATIONS, client


def test_search():
    total, results = client.search(
        query="accident de voiture",
        operator=JudilibreOperatorEnum.exact_operator,
        page_number=0,
        page_size=25,
        verbose=False,
    )

    assert total == 41
    assert len(results) == 25

    for r in results:
        assert isinstance(r, JudilibreSearchResult)
        assert "accident" in "".join(r.highlights.text).lower(), "".join(r.highlights.text)
        assert "voiture" in "".join(r.highlights.text).lower(), "".join(r.highlights.text)


@pytest.mark.parametrize(
    "jurisdiction",
    JURISDICTIONS,
)
def test_search_jurisdiction(jurisdiction):
    total, results = client.search(
        query="peuple",
        jurisdictions=[jurisdiction],
        page_number=0,
        page_size=9,
    )

    n_results = len(results)

    assert n_results == 9
    for r in results:
        assert isinstance(r, JudilibreSearchResult)
        assert r.jurisdiction == jurisdiction


@pytest.mark.parametrize(
    "jurisdiction,location",
    zip(JURISDICTIONS[1:], LOCATIONS),
)
def test_search_location(jurisdiction, location):
    total, results = client.search(
        query="peuple",
        jurisdictions=[jurisdiction],
        locations=[location],
        page_number=0,
        page_size=9,
    )

    n_results = len(results)

    assert n_results == 9
    for r in results:
        assert isinstance(r, JudilibreSearchResult)
        assert r.jurisdiction == jurisdiction
        assert r.location == location


# @pytest.mark.skip("L'erreur semble venir de l'API")
def test_search_selection():
    total, results = client.search(
        query="peuple",
        selection=True,
        jurisdictions=[j for j in JurisdictionEnum],
        page_number=0,
        page_size=9,
    )

    n_results = len(results)

    assert n_results == 9
    for r in results:
        assert isinstance(r, JudilibreSearchResult)
        selection = r.particularInterest
        assert selection


def test_search_min_date():
    # MIN DATE
    min_date = datetime.date(
        year=2000,
        month=1,
        day=1,
    )
    total, results = client.search(
        query="peuple",
        date_start=min_date,
        page_number=0,
        page_size=9,
    )

    n_results = len(results)

    assert n_results == 9
    for r in results:
        assert isinstance(r, JudilibreSearchResult)
        assert r.decision_date >= min_date


def test_search_max_date():
    # MAX DATE
    max_date = datetime.date(
        year=2000,
        month=1,
        day=1,
    )
    total, results = client.search(
        query="peuple",
        date_end=max_date,
        page_number=0,
        page_size=9,
    )

    n_results = len(results)

    assert n_results == 9
    for r in results:
        assert isinstance(r, JudilibreSearchResult)
        assert r.decision_date < max_date


def test_search_both_dates():
    min_date = datetime.date(
        year=2020,
        month=1,
        day=1,
    )
    max_date = datetime.date(
        year=2024,
        month=1,
        day=1,
    )

    total, results = client.search(
        query="peuple",
        date_start=min_date,
        date_end=max_date,
        page_number=0,
        page_size=9,
    )

    n_results = len(results)

    assert n_results == 9
    for r in results:
        assert isinstance(r, JudilibreSearchResult)
        assert (r.decision_date < max_date) and (r.decision_date >= min_date)


def test_paginate_search():
    query = "Uber"
    operator = JudilibreOperatorEnum.exact_operator
    jurisdictions = [JurisdictionEnum.cour_de_cassation]

    total, results_search = client.search(
        query=query,
        operator=operator,
        jurisdictions=jurisdictions,
        page_size=1,
    )

    results_paginate_search = client.paginate_search(
        query=query,
        operator=operator,
        jurisdictions=jurisdictions,
        max_results=None,
    )

    n_results = len(results_paginate_search)

    assert total == n_results

    for r in results_paginate_search:
        assert isinstance(r, JudilibreSearchResult)


def test_paginate_search_with_max_results():
    max_results = 10

    decisions = client.paginate_search(
        query="peuple",
        max_results=max_results,
    )

    n_decisions = len(decisions)

    assert max_results == n_decisions
