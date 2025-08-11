import pytest
import datetime
from collections import Counter

from pyjudilibre.pyjudilibre import JudilibreClient
from pyjudilibre.enums import (
    JurisdictionEnum,
    JudilibreStatsAggregationKeysEnum,
)
from pyjudilibre.models import JudilibreDecision


from .config import client

min_date = datetime.date(
    year=2020,
    month=1,
    day=1,
)
max_date = datetime.date(
    year=2020,
    month=3,
    day=1,
)
jurisdictions = [
    JurisdictionEnum.cours_d_appel,
]


@pytest.fixture(scope="module")
def decisions() -> list[JudilibreDecision]:
    return client.export_paginate(
        jurisdictions=jurisdictions,  # type: ignore
        date_start=min_date,
        date_end=max_date,
    )


def test_stats(decisions):
    stats = client.stats(
        date_start=min_date,
        date_end=max_date,
        jurisdictions=jurisdictions,  # type: ignore
    )

    decisions_min_date = min([d.decision_date for d in decisions])
    decisions_max_date = max([d.decision_date for d in decisions])
    n_decisions = len(decisions)

    assert stats.query.date_start == min_date
    assert stats.query.date_end == max_date
    assert stats.query.jurisdiction == jurisdictions[0]

    assert n_decisions == stats.results.total_decisions
    assert decisions_min_date == stats.results.min_decision_date
    assert decisions_max_date == stats.results.max_decision_date


def test_stats_aggregated_by_month(decisions):
    stats = client.stats(
        date_start=min_date,
        date_end=max_date,
        jurisdictions=jurisdictions,  # type: ignore
        keys=[JudilibreStatsAggregationKeysEnum.month],
    )

    counter = Counter(str(d.decision_date)[:7] for d in decisions)
    decision_aggregated_data = [
        {
            "key": {"month": k},
            "decisions_count": counter[k],
        }
        for k in sorted(counter.keys())
    ]

    stats_aggregated_data = [d.model_dump() for d in stats.results.aggregated_data]

    assert decision_aggregated_data == stats_aggregated_data


def test_stats_aggregated_by_location(decisions):
    stats = client.stats(
        date_start=min_date,
        date_end=max_date,
        jurisdictions=jurisdictions,  # type: ignore
        keys=[JudilibreStatsAggregationKeysEnum.location],
    )

    counter = Counter(d.location.values[1] for d in decisions)
    decision_aggregated_data = [
        {
            "key": {"location": k},
            "decisions_count": counter[k],
        }
        for k in sorted(counter.keys())
    ]
    stats_aggregated_data = [d.model_dump() for d in stats.results.aggregated_data]

    assert decision_aggregated_data == stats_aggregated_data
