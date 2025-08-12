import datetime

import pytest
from pyjudilibre.enums import JurisdictionEnum
from pyjudilibre.models import JudilibreSearchResult

from .config import client


def test_search():
    total, results = client.search(
        query="accident de voiture",
        operator="exact",
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
    [r for r in JurisdictionEnum],
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
    # MIN DATE
    min_date = datetime.date(
        year=2020,
        month=1,
        day=1,
    )

    # MAX DATE
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


def test_search_paginate():
    query = "Uber"
    operator = "and"
    jurisdictions = [JurisdictionEnum.cour_de_cassation]

    total, results_search = client.search(
        query=query,
        operator=operator,
        jurisdictions=jurisdictions,
        page_size=1,
    )

    results_paginate_search = client.search_paginate(
        query=query,
        operator=operator,
        jurisdictions=jurisdictions,
        max_results=None,
    )

    n_results = len(results_paginate_search)

    assert total == n_results

    for r in results_paginate_search:
        assert isinstance(r, JudilibreSearchResult)


def test_search_paginate_with_max_results():
    max_results = 10

    decisions = client.search_paginate(
        query="peuple",
        max_results=max_results,
    )

    n_decisions = len(decisions)

    assert max_results == n_decisions
