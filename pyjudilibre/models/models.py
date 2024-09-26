from typing import Optional, Union

from pydantic import BaseModel, ConfigDict

from .enums import LocationCAEnum, LocationTJEnum, SourceEnum, JurisdictionEnum


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
    rawUrl: Optional[str] = None


class ShortDecision(BaseModel):
    """Class that represents a decision with only a few information

    Args:
        id (Optional[str]): id of the decision if the decision is in Judilibre.
        date (str): date of the decision (YYYY-MM-DD).
        jurisdiction (str): name of the jurisdiction.
        chamber (Optional[str]): name of the chamber in the jurisdiction.
        title (str): combination of the name of the jurisdiction and the chamber.
        solution (Optional[str]): solution of the decision.
        number (str): register number of the decision
    """

    id: Optional[str] = None
    date: str
    jurisdiction: Optional[str] = None
    chamber: Optional[str] = None
    title: str
    solution: Optional[str] = None
    number: Optional[str] = None


class Article(BaseModel):
    """Class that represents an article of the law or a decision.

    Args:
        title (str): denomination of the article.
    """

    title: str


class Legacy(BaseModel):
    """Class

    Args:
        matiereDeterminee (Optional[int]): ...
        pourvoiLocal (Optional[int]): ...
        pourvoiCcas (Optional[int]): ...
        pourvoiLocal (Optional[int]): ...
        pourvoiCcas (Optional[int]): ...
    """

    matiereDeterminee: Optional[int] = None
    pourvoiLocal: Optional[int] = None
    pourvoiCcas: Optional[int] = None
    pourvoiLocal: Optional[int] = None
    pourvoiCcas: Optional[int] = None


class JudilibreShortDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # Mandatory attributes
    ## decision attributes
    id: str
    decision_date: str
    jurisdiction: Optional[JurisdictionEnum] = None 
    number: str
    numbers: list[str]
    publication: list[str]
    solution: str  # TODO: remplacer par SolutionEnum
    particularInterest: bool

    # Optional values
    location: Optional[Union[LocationCAEnum, LocationTJEnum]] = None
    chamber: Optional[str] = None
    ecli: Optional[str] = None
    formation: Optional[str] = None  # remplacer par FormationEnum ?
    type: Optional[str] = None
    solution_alt: Optional[str] = None
    summary: Optional[str] = None
    bulletin: Optional[str] = None
    files: Optional[list] = None  # TODO: completer ces schémas
    themes: Optional[list] = None  # TODO: completer ces schémas
    titlesAndSummaries: Optional[list[dict]] = None  # TODO: completer ces schémas


class Highlights(BaseModel):
    text: list[str] = []


class SearchResult(JudilibreShortDecision):
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
        ecli (Optional[str]): ECLI id
        publication (list[str]): list of publication types
        decision_date (str): date of the decision (YYYY-MM-DD)
        update_date (str): date of the last update of the decision (YYYY-MM-DD)
        update_datetime (str): datetime of the last update (YYYY-MM-DD 00:00:00+0)
        decision_datetime (str): datetime of the decision (YYYY-MM-DD 00:00:00+0)
        solution (SolutionEnum): solution of the decision
        type (str): type of the decision
        themes (Optional[list[str]]): list of themes of the decision (CCass)
        nac (Optional[str]): code of the nature of the decision (CA)
        portalis (Optional[str]): portalis number of the decision
        files (list[File]): list of files
        zones (Optional[Zones]): dictionary of computed zones of the decision
        contested (Optional[ShortDecision]): ...
        forward (Optional[str]): ...
        timeline (Optional[list[ShortDecision]]): list of related decisions
        partial (str): ...
        visa (list[Article]): list of law articles to base the pourvoi on
        rapprochements (list[Article]): list of decisions related to this decision
        legacy (Legacy): ...
    """

    source: SourceEnum
    text: str
    update_date: str
    update_datetime: Optional[str] = None
    decision_datetime: Optional[str] = None
    themes: Optional[list[str]] = None
    nac: Optional[str] = None
    portalis: Optional[str] = None
    files: Optional[list[File]] = None
    zones: Optional[Zones] = None
    contested: Optional[ShortDecision] = None
    forward: Optional[str] = None
    timeline: Optional[list[ShortDecision]] = None
    partial: Optional[bool] = None
    visa: Optional[list[Article]] = None
    rapprochements: Optional[list[Article]] = None
    legacy: Optional[Legacy] = None


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
