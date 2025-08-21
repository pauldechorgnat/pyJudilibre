import datetime

import pytest
from pyjudilibre.enums import JurisdictionEnum
from pyjudilibre.models import JudilibreDecision

from .config import JURISDICTIONS, LOCATIONS, client


def test_scan():
    total, decisions, search_after = client.scan(batch_size=12)

    n_decisions = len(decisions)
    assert n_decisions == 12

    for d in decisions:
        assert isinstance(d, JudilibreDecision)


@pytest.mark.parametrize(
    "jurisdiction",
    JURISDICTIONS,
)
def test_scan_jurisdiction(jurisdiction):
    total, decisions, search_after = client.scan(
        batch_size=12,
        jurisdictions=[jurisdiction],
    )

    n_decisions = len(decisions)
    assert n_decisions == 12
    for d in decisions:
        assert isinstance(d, JudilibreDecision)
        assert d.jurisdiction == jurisdiction


@pytest.mark.parametrize(
    "jurisdiction, location",
    zip(JURISDICTIONS[1:], LOCATIONS),
)
def test_scan_location(jurisdiction, location):
    total, decisions, search_after = client.scan(
        batch_size=12,
        jurisdictions=[jurisdiction],
        locations=[location],
    )

    n_decisions = len(decisions)
    assert n_decisions == 12
    for d in decisions:
        assert isinstance(d, JudilibreDecision)
        assert d.jurisdiction == jurisdiction
        assert d.location == location


def test_scan_paginate():
    # stats
    min_date = datetime.date(
        year=2024,
        month=1,
        day=1,
    )
    max_date = datetime.date(
        year=2025,
        month=1,
        day=1,
    )

    stats = client.stats(
        jurisdictions=[JurisdictionEnum.cour_de_cassation],
        date_start=min_date,
        date_end=max_date,
    )

    decisions = client.paginate_scan(
        jurisdictions=[JurisdictionEnum.cour_de_cassation],
        date_start=min_date,
        date_end=max_date,
    )

    n_decisions = len(decisions)

    assert n_decisions == stats.results.total_decisions

    for d in decisions:
        assert isinstance(d, JudilibreDecision)
        assert d.jurisdiction == JurisdictionEnum.cour_de_cassation
        assert d.decision_date >= min_date
        assert d.decision_date <= max_date


def test_scan_paginate_with_max_results():
    decisions = client.paginate_scan(
        jurisdictions=[JurisdictionEnum.cour_de_cassation],
        max_results=12,
    )

    n_decisions = len(decisions)

    assert n_decisions == 12

    for d in decisions:
        assert d.jurisdiction == JurisdictionEnum.cour_de_cassation
