import pytest

from pyjudilibre.enums import JurisdictionEnum, SourceEnum
from pyjudilibre.models import JudilibreShortDecision

from .config import client


@pytest.mark.parametrize(
    "jurisdiction",
    [j for j in JurisdictionEnum],
)
def test_abridged_by_jurisdiction(jurisdiction):
    total, decisions, _ = client.scan(
        batch_size=12,
        abridged=True,
        jurisdictions=[jurisdiction],
    )
    n_decisions = len(decisions)

    assert n_decisions == 12

    for d in decisions:
        assert isinstance(d, JudilibreShortDecision)
        assert d.jurisdiction == jurisdiction


@pytest.mark.parametrize(
    "source",
    [s for s in SourceEnum],
)
def test_abridged_by_source(source):
    total, decisions, _ = client.scan(
        batch_size=12,
        abridged=True,
        sources=[source],
    )

    n_decisions = len(decisions)

    assert n_decisions == 12
    for d in decisions:
        assert isinstance(d, JudilibreShortDecision)


def test_abridged_export():
    total, decisions = client.export(
        batch_size=12,
        batch_number=0,
        abridged=True,
    )

    n_decisions = len(decisions)

    assert n_decisions == 12
    for d in decisions:
        assert isinstance(d, JudilibreShortDecision)


def test_abridged_scan():
    total, decisions, _ = client.scan(
        batch_size=12,
        abridged=True,
    )

    n_decisions = len(decisions)

    assert n_decisions == 12
    for d in decisions:
        assert isinstance(d, JudilibreShortDecision)


def test_abridged_paginate_export():
    decisions = client.paginate_export(
        max_results=1001,
        abridged=True,
        timeout=20,
    )

    n_decisions = len(decisions)

    assert n_decisions == 1001

    for d in decisions:
        assert isinstance(d, JudilibreShortDecision)


def test_abridged_paginate_scan():
    decisions = client.paginate_scan(
        max_results=1001,
        abridged=True,
        timeout=20,
    )

    n_decisions = len(decisions)

    assert n_decisions == 1001
    for d in decisions:
        assert isinstance(d, JudilibreShortDecision)
