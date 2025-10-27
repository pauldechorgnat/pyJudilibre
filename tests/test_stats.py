import datetime
from collections import Counter

import pytest

from pyjudilibre.enums import (
    JudilibreDateTypeEnum,
    JudilibreStatsAggregationKeysEnum,
    JurisdictionEnum,
)
from pyjudilibre.models import (
    JudilibreAggregatedData,
    JudilibreDecision,
    JudilibreShortDecision,
    JudilibreStatsAggregationKey,
)

from .config import client

start_date = datetime.date(year=2024, month=12, day=25)
end_date = datetime.date(year=2025, month=1, day=10)
jurisdictions = [
    j
    for j in JurisdictionEnum
    if j
    not in [
        JurisdictionEnum.tribunaux_judiciaires,
        JurisdictionEnum.tribunaux_de_commerce,
    ]
]

# YEAR, MONTH -> CC
# SPECIFIC CC -> CC
# JURISDICTIONS, LOCATIONS, PARTICULAR INTEREST -> CA, TJ, TCOM


@pytest.fixture(scope="module")
def decisions_all() -> list[JudilibreDecision] | list[JudilibreShortDecision]:
    decisions = client.paginate_scan(
        jurisdictions=jurisdictions,
        date_start=start_date,
        date_end=end_date,
        batch_size=1000,
        date_type=JudilibreDateTypeEnum.creation,
    )

    return decisions


@pytest.fixture(scope="module")
def decisions_cc(decisions_all) -> list[JudilibreDecision]:
    return list(
        filter(
            lambda d: d.jurisdiction == JurisdictionEnum.cour_de_cassation,
            decisions_all,
        )
    )


@pytest.fixture(scope="module")
def decisions_ca(decisions_all) -> list[JudilibreDecision]:
    return list(
        filter(
            lambda d: d.jurisdiction == JurisdictionEnum.cours_d_appel,
            decisions_all,
        )
    )


def test_stats_aggregated_by_month(decisions_cc):
    stats = client.stats(
        date_start=start_date,
        date_end=end_date,
        jurisdictions=[JurisdictionEnum.cour_de_cassation],
        keys=[JudilibreStatsAggregationKeysEnum.month],
        date_type=JudilibreDateTypeEnum.creation,
    )

    counter = Counter(str(d.decision_date)[:7] for d in decisions_cc)
    decision_aggregated_data = [
        JudilibreAggregatedData(
            **{
                "key": {"month": k},
                "decisions_count": counter[k],
            }
        )
        for k in sorted(counter.keys())
    ]

    stats_aggregated_data = stats.results.aggregated_data

    assert decision_aggregated_data == stats_aggregated_data


def test_stats_aggregated_by_year(decisions_all):
    decisions_cc = list(
        filter(
            lambda d: d.jurisdiction == JurisdictionEnum.cour_de_cassation,
            decisions_all,
        )
    )
    stats = client.stats(
        date_start=start_date,
        date_end=end_date,
        jurisdictions=[JurisdictionEnum.cour_de_cassation],
        keys=[JudilibreStatsAggregationKeysEnum.year],
        date_type=JudilibreDateTypeEnum.creation,
    )

    counter = Counter(str(d.decision_date)[:4] for d in decisions_cc)
    decision_aggregated_data = [
        JudilibreAggregatedData(
            **{
                "key": {"year": k},
                "decisions_count": counter[k],
            }
        )
        for k in sorted(counter.keys())
    ]
    stats_aggregated_data = stats.results.aggregated_data

    assert decision_aggregated_data == stats_aggregated_data


def test_stats_aggregated_by_jurisdiction(decisions_all):
    stats = client.stats(
        date_start=start_date,
        date_end=end_date,
        jurisdictions=jurisdictions,
        keys=[JudilibreStatsAggregationKeysEnum.jurisdiction],
        date_type=JudilibreDateTypeEnum.creation,
    )

    counter = Counter(d.jurisdiction.value for d in decisions_all)
    decision_aggregated_data = [
        JudilibreAggregatedData(
            **{
                "key": {"jurisdiction": k},
                "decisions_count": counter[k],
            }
        )
        for k in sorted(counter.keys())
    ]

    stats_aggregated_data = stats.results.aggregated_data

    assert decision_aggregated_data == stats_aggregated_data


def test_stats_aggregated_by_location(decisions_ca):
    stats = client.stats(
        date_start=start_date,
        date_end=end_date,
        jurisdictions=[JurisdictionEnum.cours_d_appel],
        keys=[JudilibreStatsAggregationKeysEnum.location],
        date_type=JudilibreDateTypeEnum.creation,
    )

    counter = Counter(d.location.value for d in decisions_ca if d.location)
    decision_aggregated_data = [
        JudilibreAggregatedData(
            **{
                "key": {"location": k},
                "decisions_count": counter[k],
            }
        )
        for k in sorted(counter.keys())
    ]

    stats_aggregated_data = sorted(
        stats.results.aggregated_data,
        key=lambda d: d.key.location.value if d.key.location else "",
    )
    assert decision_aggregated_data == stats_aggregated_data


def test_stats_aggregated_by_formation(decisions_cc):
    stats = client.stats(
        date_start=start_date,
        date_end=end_date,
        jurisdictions=[JurisdictionEnum.cour_de_cassation],
        keys=[JudilibreStatsAggregationKeysEnum.formation],
        date_type=JudilibreDateTypeEnum.creation,
    )

    counter = Counter(d.formation for d in decisions_cc if d.formation)

    expected_stats = [
        JudilibreAggregatedData(
            key=JudilibreStatsAggregationKey(formation=formation),
            decisions_count=counter[formation],
        )
        for formation in sorted(
            counter.keys(),
            key=lambda x: x.value if x else "",
        )
    ]

    computed_stats = sorted(
        stats.results.aggregated_data,
        key=lambda x: x.key.formation.value if x.key.formation else "",
    )

    assert expected_stats == computed_stats


def test_stats_aggregated_by_chamber(decisions_cc):
    stats = client.stats(
        date_start=start_date,
        date_end=end_date,
        jurisdictions=[JurisdictionEnum.cour_de_cassation],
        keys=[JudilibreStatsAggregationKeysEnum.chamber],
        date_type=JudilibreDateTypeEnum.creation,
    )

    counter = Counter(d.chamber for d in decisions_cc if d.chamber)

    expected_stats = [
        JudilibreAggregatedData(
            key=JudilibreStatsAggregationKey(chamber=chamber),
            decisions_count=counter[chamber],
        )
        for chamber in sorted(
            counter.keys(),
            key=lambda x: str(x) if x else "",
        )
    ]

    computed_stats = sorted(
        stats.results.aggregated_data,
        key=lambda x: str(x.key.chamber) if x.key.chamber else "",
    )

    assert expected_stats == computed_stats


def test_stats_aggregated_by_publication(decisions_cc):
    stats = client.stats(
        date_start=start_date,
        date_end=end_date,
        jurisdictions=[JurisdictionEnum.cour_de_cassation],
        keys=[JudilibreStatsAggregationKeysEnum.publication],
        date_type=JudilibreDateTypeEnum.creation,
    )

    counter = Counter(p for d in decisions_cc for p in d.publication)

    expected_stats = [
        JudilibreAggregatedData(
            key=JudilibreStatsAggregationKey(publication=publication),
            decisions_count=counter[publication],
        )
        for publication in sorted(
            counter.keys(),
            key=lambda x: x.value if x else "",
        )
    ]

    computed_stats = sorted(
        stats.results.aggregated_data,
        key=lambda x: x.key.publication.value if x.key.publication else "",
    )

    assert expected_stats == computed_stats


# def test_stats_aggregated_by_theme(decisions_cc):
#     stats = client.stats(
#         date_start=start_date,
#         date_end=end_date,
#         jurisdictions=[JurisdictionEnum.cour_de_cassation],
#         keys=[JudilibreStatsAggregationKeysEnum.themes],
#         date_type=JudilibreDateTypeEnum.creation,
#     )

#     counter = Counter(t for d in decisions_cc for t in d.themes)

#     expected_stats = [
#         JudilibreAggregatedData(
#             key=JudilibreStatsAggregationKey(theme=theme),
#             decisions_count=counter[theme],
#         )
#         for theme in sorted(
#             counter.keys(),
#             key=lambda x: x if x else "",
#         )
#     ]

#     computed_stats = sorted(
#         stats.results.aggregated_data,
#         key=lambda x: x.key.theme if x.key.theme else "",
#     )

#     assert expected_stats == computed_stats


def test_stats_aggregated_by_solution(decisions_cc):
    stats = client.stats(
        date_start=start_date,
        date_end=end_date,
        jurisdictions=[JurisdictionEnum.cour_de_cassation],
        keys=[JudilibreStatsAggregationKeysEnum.solution],
        date_type=JudilibreDateTypeEnum.creation,
    )

    counter = Counter(d.solution for d in decisions_cc if d.solution)

    expected_stats = [
        JudilibreAggregatedData(
            key=JudilibreStatsAggregationKey(solution=solution),
            decisions_count=counter[solution],
        )
        for solution in sorted(
            counter.keys(),
            key=lambda x: str(x) if x.value else "",
        )
    ]

    computed_stats = sorted(
        stats.results.aggregated_data,
        key=lambda x: str(x.key.solution) if x.key.solution else "",
    )

    assert expected_stats == computed_stats


def test_stats_aggregated_by_nac(decisions_ca):
    stats = client.stats(
        date_start=start_date,
        date_end=end_date,
        jurisdictions=[JurisdictionEnum.cours_d_appel],
        keys=[JudilibreStatsAggregationKeysEnum.nac],
        date_type=JudilibreDateTypeEnum.creation,
    )

    counter = Counter(d.nac for d in decisions_ca if d.nac)

    expected_stats = [
        JudilibreAggregatedData(
            key=JudilibreStatsAggregationKey(nac=nac),
            decisions_count=counter[nac],
        )
        for nac in sorted(
            counter.keys(),
            key=lambda x: str(x) if x else "",
        )
    ]

    computed_stats = sorted(
        stats.results.aggregated_data,
        key=lambda x: str(x.key.nac) if x.key.nac else "",
    )

    assert expected_stats == computed_stats
