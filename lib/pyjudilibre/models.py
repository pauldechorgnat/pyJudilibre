import datetime

from pydantic import BaseModel, ConfigDict
from pyjudilibre.enums import (
    JudilibreStatsAggregationKeysEnum,
    JudilibreTransactionActionEnum,
    JurisdictionEnum,
    LocationCAEnum,
    LocationTCOMEnum,
    LocationTJEnum,
    SourceEnum,
)


class Zone(BaseModel):
    """Represents a zone in the text of a decision.
    Args:
        start (int): index of the start of the zone.
        end (int): index of the end of the zone.
    """

    start: int
    end: int


class Zones(BaseModel):
    """Class that represents the zones that can be found in the text of a decision.

    Args:
        introduction (list[Zone]): list of introduction zones. Can be empty.
        moyens (list[Zone]): list of moyens zones. Can be empty.
        dispositif (list[Zone]): list of dispositif zones. Can be empty.
        expose (list[Zone]): list of expose du litige zones. Can be empty.
        motivations (list[Zone]): list of motivations zones. Can be empty.
        annexes (list[Zone]): list of annexes zones. Can be empty.
    """

    introduction: list[Zone] = []
    moyens: list[Zone] = []
    dispositif: list[Zone] = []
    expose: list[Zone] = []
    motivations: list[Zone] = []
    annexes: list[Zone] = []


class File(BaseModel):
    """
    Class that represents a file that can be associated with a decision.

    Args:
        id (str): id of the file.
        type (str): type of the file.
        isCommunication (bool): boolean to indicate if a file is a communiqué.
        date (str): date of issue of the file (YYYY-MM-DD).
        name (str): name of the file.
        size (str): size of the file.
        url (str): general URL of the file.
        rawUrl (str): url of the file.

    """

    id: str
    type: str
    isCommunication: bool
    date: str
    name: str
    size: str
    url: str
    rawUrl: str | None = None


class ShortDecision(BaseModel):
    """Class that represents a decision with only a few information

    Args:
        id (str | None): id of the decision if the decision is in Judilibre.
        date (str): date of the decision (YYYY-MM-DD).
        jurisdiction (str): name of the jurisdiction.
        chamber (str | None): name of the chamber in the jurisdiction.
        title (str): combination of the name of the jurisdiction and the chamber.
        solution (str | None): solution of the decision.
        number (str): register number of the decision
    """

    id: str | None = None
    date: str
    jurisdiction: str | None = None
    chamber: str | None = None
    title: str
    solution: str | None = None
    number: str | None = None


class Article(BaseModel):
    """Class that represents an article of the law or a decision.

    Args:
        title (str): denomination of the article.
    """

    title: str


class Legacy(BaseModel):
    """Class

    Args:
        matiereDeterminee (int | None): ...
        pourvoiLocal (int | None): ...
        pourvoiCcas (int | None): ...
        pourvoiLocal (int | None): ...
        pourvoiCcas (int | None): ...
    """

    matiereDeterminee: int | None = None
    pourvoiLocal: int | None = None
    pourvoiCcas: int | None = None


class JudilibreShortDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # Mandatory attributes
    ## decision attributes
    id: str
    decision_date: datetime.date
    jurisdiction: JurisdictionEnum | None = None
    number: str
    numbers: list[str]
    publication: list[str] | None = None
    solution: str | None = None  # TODO: remplacer par SolutionEnum
    particularInterest: bool

    # Optional values
    location: LocationCAEnum | LocationTJEnum | LocationTCOMEnum | None = None
    chamber: str | None = None
    ecli: str | None = None
    formation: str | None = None  # remplacer par FormationEnum ?
    type: str | None = None
    solution_alt: str | None = None
    summary: str | None = None
    bulletin: str | None = None
    files: list | None = None  # TODO: completer ces schémas
    themes: list | None = None  # TODO: completer ces schémas
    titlesAndSummaries: list[dict] | None = None  # TODO: completer ces schémas


class Highlights(BaseModel):
    text: list[str] = []


class JudilibreSearchResult(JudilibreShortDecision):
    # Mandatory attributes
    ## Search attributes
    score: float
    highlights: Highlights  # TODO: completer ces schémas


class JudilibreDecision(JudilibreShortDecision):
    """
    Args:
        id (str): id of the decision
        source (SourceEnum): data source of the decision
        text (str): pseudonymized text of the decision
        jurisdiction (JurisdictionLevelEnum): jurisdiction of the decision
        chamber (str): chamber of the decision within the jurisdiction
        number (str): register number of the decision
        numbers (list[str]): list of alternative register numbers of the decision
        ecli (str | None): ECLI id
        publication (list[str]): list of publication types
        decision_date (str): date of the decision (YYYY-MM-DD)
        update_date (str): date of the last update of the decision (YYYY-MM-DD)
        update_datetime (str): datetime of the last update (YYYY-MM-DD 00:00:00+0)
        decision_datetime (str): datetime of the decision (YYYY-MM-DD 00:00:00+0)
        solution (SolutionEnum): solution of the decision
        type (str): type of the decision
        themes (Optional[list[str]]): list of themes of the decision (CCass)
        nac (str | None): code of the nature of the decision (CA)
        portalis (str | None): portalis number of the decision
        files (list[File]): list of files
        zones (Optional[Zones]): dictionary of computed zones of the decision
        contested (Optional[ShortDecision]): ...
        forward (str | None): ...
        timeline (Optional[list[ShortDecision]]): list of related decisions
        partial (str): ...
        visa (list[Article]): list of law articles to base the pourvoi on
        rapprochements (list[Article]): list of decisions related to this decision
        legacy (Legacy): ...
    """

    source: SourceEnum
    text: str
    update_date: str
    update_datetime: str | None = None
    decision_datetime: str | None = None
    themes: list[str] | None = None
    nac: str | None = None
    portalis: str | None = None
    files: list[File] | None = None
    zones: Zones | None = None
    contested: ShortDecision | None = None
    forward: str | dict | None = None
    timeline: list[ShortDecision] | None = None
    partial: bool | None = None
    visa: list[Article] | None = None
    rapprochements: list[Article] | None = None
    legacy: Legacy | None = None


class JudilibreAggregatedData(BaseModel):
    key: dict
    decisions_count: int


class JudilibreStatsResults(BaseModel):
    min_decision_date: datetime.date
    max_decision_date: datetime.date
    total_decisions: int
    aggregated_data: list[JudilibreAggregatedData] = []


class JudilibreStatsQuery(BaseModel):
    date_start: datetime.date | None = None
    date_end: datetime.date | None = None
    jurisdiction: JurisdictionEnum | None = None
    location: LocationCAEnum | LocationTJEnum | LocationTCOMEnum | None = None
    selection: bool | None = None

    keys: list[JudilibreStatsAggregationKeysEnum] | JudilibreStatsAggregationKeysEnum | None = None


class JudilibreStats(BaseModel):
    results: JudilibreStatsResults
    query: JudilibreStatsQuery


class JudilibreTransaction(BaseModel):
    id: str
    action: JudilibreTransactionActionEnum
    date: datetime.datetime


dummy_short_decision = {
    "id": "123456",
    "decision_date": "2023-01-01",
    "jurisdiction": "cc",
    "chamber": "CRIM",
    "number": "123456",
    "numbers": ["123456"],
    "publication": ["P"],
    "solution": "rejet",
    "particularInterest": False,
    # "source": "jurinet",
    # "text": "AU NOM DU PEUPLE FRANCAIS",
}
