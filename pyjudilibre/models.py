from enum import Enum
from typing import Union

from pydantic import BaseModel


class SourceEnum(Enum):
    """Data source of a decision.

    Can only take one of 3 values:
    - 'jurinet': Cour de cassation system.
    - 'jurica': Cours d'appel system.
    - 'dila': Legacy system.
    """

    jurinet = "jurinet"
    jurica = "jurica"
    dila = "dila"


class JurisdictionLevelEnum(Enum):
    """Jurisdiction level of a decision.

    Can only take one of 2 values:
    - 'cc' for Cour de cassation.
    - 'ca' for Cour d'appel.
    """

    cour_de_cassation = "cc"
    cours_d_appel = "ca"


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
    rawUrl: str


class ShortDecision(BaseModel):
    """Class that represents a decision with only a few information

    Args:
        id (Union[str, None]): id of the decision if the decision is in Judilibre.
        date (str): date of the decision (YYYY-MM-DD).
        jurisdiction (str): name of the jurisdiction.
        chamber (Union[str, None]): name of the chamber in the jurisdiction.
        title (str): combination of the name of the jurisdiction and the chamber.
        solution (Union[str, None]): solution of the decision.
        number (str): register number of the decision
    """

    id: Union[str, None]
    date: str
    jurisdiction: str
    chamber: Union[str, None]
    title: str
    solution: Union[str, None]
    number: str


class Article(BaseModel):
    """Class that represents an article of the law or a decision.

    Args:
        title (str): denomination of the article.
    """

    title: str


class Legacy(BaseModel):
    """Class

    Args:
        matiereDeterminee (Union[int, None]): ...
        pourvoiLocal (Union[int, None]): ...
        pourvoiCcas (Union[int, None]): ...
        pourvoiLocal (Union[int, None]): ...
        pourvoiCcas (Union[int, None]): ...
    """

    matiereDeterminee: Union[int, None]
    pourvoiLocal: Union[int, None]
    pourvoiCcas: Union[int, None]
    pourvoiLocal: Union[int, None]
    pourvoiCcas: Union[int, None]


class JudilibreDecision(BaseModel):
    """
    Args:
        id (str): id of the decision
        source (SourceEnum): data source of the decision
        text (str): pseudonymized text of the decision
        jurisdiction (JurisdictionLevelEnum): jurisdiction of the decision
        chamber (str): chamber of the decision within the jurisdiction
        number (str): register number of the decision
        numbers (list[str]): list of alternative register numbers of the decision
        ecli (Union[str, None]): ECLI id
        publication (list[str]): list of publication types
        decision_date (str): date of the decision (YYYY-MM-DD)
        update_date (str): date of the last update of the decision (YYYY-MM-DD)
        update_datetime (str): datetime of the last update (YYYY-MM-DD 00:00:00+0)
        decision_datetime (str): datetime of the decision (YYYY-MM-DD 00:00:00+0)
        solution (str): solution of the decision
        type (str): type of the decision
        themes (Union[list[str], None]): list of themes of the decision (CCass)
        nac (Union[str, None]): code of the nature of the decision (CA)
        portalis (Union[str, None]): portalis number of the decision
        files (list[File]): list of files
        zones (Union[Zones, None]): dictionary of computed zones of the decision
        contested (Union[ShortDecision, None]): ...
        forward (Union[str, None]): ...
        timeline (Union[list[ShortDecision], None]): list of related decisions
        partial (str): ...
        visa (list[Article]): list of law articles to base the pourvoi on
        rapprochements (list[Article]): list of decisions related to this decision
        legacy (Legacy): ...
    """

    id: str
    source: SourceEnum
    text: str
    jurisdiction: JurisdictionLevelEnum
    chamber: str
    number: str
    numbers: list[str]
    ecli: Union[str, None]
    publication: list[str]
    decision_date: str
    update_date: str
    update_datetime: str
    decision_datetime: str
    solution: str
    type: str
    themes: Union[list[str], None]
    nac: Union[str, None]
    portalis: Union[str, None]
    files: list[File]
    zones: Union[Zones, None]
    contested: Union[ShortDecision, None]
    forward: Union[str, None]
    timeline: Union[list[ShortDecision], None]
    partial: str
    visa: list[Article]
    rapprochements: list[Article]
    legacy: Legacy
