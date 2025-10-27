from pyjudilibre.enums import ZoneTypeEnum
from pyjudilibre.models import (
    JudilibreDecision,
    ZoneWithText,
    test_decision_data,
)


def test_zoning():
    text = (
        "A" * 10  # introduction
        + "B" * 10  # expose du litige
        + "C" * 10  # moyen 1
        + "D" * 10  # motivation 1
        + "E" * 10  # moyen 2
        + "F" * 10  # motivation 2
        + "G" * 10  # dispositif
        + "H" * 10
    )

    zones = {
        "introduction": [
            {"start": 0, "end": 10},
        ],
        "expose": [
            {"start": 10, "end": 20},
        ],
        "moyens": [
            {"start": 20, "end": 30},
            {"start": 40, "end": 50},
        ],
        "motivations": [
            {"start": 30, "end": 40},
            {"start": 50, "end": 60},
        ],
        "dispositif": [
            {"start": 60, "end": 70},
        ],
        "annexes": [
            {"start": 70, "end": 80},
        ],
    }

    decision = JudilibreDecision(
        **{
            **test_decision_data,
            "text": text,
            "zones": zones,
        }
    )

    zoning = [
        ZoneWithText(start=0, end=10, text="A" * 10, type=ZoneTypeEnum.introduction),
        ZoneWithText(start=10, end=20, text="B" * 10, type=ZoneTypeEnum.expose_du_litige),
        ZoneWithText(start=20, end=30, text="C" * 10, type=ZoneTypeEnum.moyen),
        ZoneWithText(start=30, end=40, text="D" * 10, type=ZoneTypeEnum.motivation),
        ZoneWithText(start=40, end=50, text="E" * 10, type=ZoneTypeEnum.moyen),
        ZoneWithText(start=50, end=60, text="F" * 10, type=ZoneTypeEnum.motivation),
        ZoneWithText(start=60, end=70, text="G" * 10, type=ZoneTypeEnum.dispositif),
        ZoneWithText(start=70, end=80, text="H" * 10, type=ZoneTypeEnum.moyen_annexe),
    ]

    assert decision.zoning.all == zoning
    assert decision.zoning.introduction == zoning[0]
    assert decision.zoning.expose_du_litige == zoning[1]
    assert decision.zoning.moyens == [zoning[2], zoning[4]]
    assert decision.zoning.motivations == [zoning[3], zoning[5]]
    assert decision.zoning.dispositif == zoning[6]
    assert decision.zoning.moyens_annexes == [zoning[7]]
