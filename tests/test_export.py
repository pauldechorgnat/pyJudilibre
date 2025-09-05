import datetime

import pytest

from pyjudilibre.enums import JurisdictionEnum
from pyjudilibre.models import JudilibreDecision

from .config import JURISDICTIONS, LOCATIONS, client


def test_export():
    total, results = client.export(
        batch_number=0,
        batch_size=42,
    )

    n_results = len(results)
    assert n_results == 42

    for r in results:
        assert isinstance(r, JudilibreDecision)


@pytest.mark.parametrize(
    "jurisdiction",
    JURISDICTIONS,
)
def test_export_jurisdiction(jurisdiction):
    total, results = client.export(
        jurisdictions=[jurisdiction],
        batch_number=0,
        batch_size=42,
    )

    n_results = len(results)
    assert n_results == 42

    for r in results:
        assert isinstance(r, JudilibreDecision)
        assert r.jurisdiction == jurisdiction


@pytest.mark.parametrize(
    "jurisdiction,location",
    zip(JURISDICTIONS[1:], LOCATIONS),
)
def test_export_location(jurisdiction, location):
    total, results = client.export(
        jurisdictions=[jurisdiction],
        locations=[location],
        batch_number=0,
        batch_size=9,
    )

    n_results = len(results)

    assert n_results == 9
    for r in results:
        assert isinstance(r, JudilibreDecision)
        assert r.jurisdiction == jurisdiction
        assert r.location == location


def test_export_selection():
    total, results = client.export(
        selection=True,
        jurisdictions=[j for j in JurisdictionEnum],
        batch_number=0,
        batch_size=9,
    )

    n_results = len(results)

    assert n_results == 9
    for r in results:
        assert isinstance(r, JudilibreDecision)
        selection = r.particularInterest
        assert selection


def test_export_min_date():
    # MIN DATE
    min_date = datetime.date(
        year=2000,
        month=1,
        day=1,
    )
    total, results = client.export(
        date_start=min_date,
        batch_number=0,
        batch_size=9,
    )

    n_results = len(results)

    assert n_results == 9
    for r in results:
        assert isinstance(r, JudilibreDecision)
        assert r.decision_date >= min_date


def test_export_max_date():
    # MAX DATE
    max_date = datetime.date(
        year=2000,
        month=1,
        day=1,
    )
    total, results = client.export(
        date_end=max_date,
        batch_number=0,
        batch_size=9,
    )

    n_results = len(results)

    assert n_results == 9
    for r in results:
        assert isinstance(r, JudilibreDecision)
        assert r.decision_date < max_date


def test_export_both_dates():
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

    total, results = client.export(
        date_start=min_date,
        date_end=max_date,
        batch_number=0,
        batch_size=9,
    )

    n_results = len(results)

    assert n_results == 9
    for r in results:
        assert isinstance(r, JudilibreDecision)
        assert (r.decision_date < max_date) and (r.decision_date >= min_date)


def test_paginate_export():
    jurisdictions = [JurisdictionEnum.cour_de_cassation]
    min_date = datetime.date(
        year=2020,
        month=1,
        day=1,
    )
    max_date = datetime.date(
        year=2020,
        month=2,
        day=1,
    )

    total, decisions = client.export(
        batch_number=0,
        batch_size=10,
        jurisdictions=jurisdictions,
        date_start=min_date,
        date_end=max_date,
        page_size=1,
    )

    decisions_paginate = client.paginate_export(
        jurisdictions=jurisdictions,
        date_start=min_date,
        date_end=max_date,
        max_results=None,
    )

    n_decisions = len(decisions_paginate)

    assert total == n_decisions

    for r in decisions_paginate:
        assert isinstance(r, JudilibreDecision)


def test_paginate_export_with_max_results():
    max_results = 10

    decisions = client.paginate_export(
        max_results=max_results,
    )

    n_decisions = len(decisions)

    assert max_results == n_decisions
