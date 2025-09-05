import datetime
import os
import urllib.request

from pydantic import BaseModel, ConfigDict, field_validator

from pyjudilibre.enums import (
    ChamberCCEnum,
    FormationCCEnum,
    JudilibreFileTypeEnum,
    JudilibreStatsAggregationKeysEnum,
    JudilibreTransactionActionEnum,
    JurisdictionEnum,
    LocationCAEnum,
    LocationTCOMEnum,
    LocationTJEnum,
    PublicationCCEnum,
    SolutionCCEnum,
    SourceEnum,
)
from pyjudilibre.exceptions import JudilibreDownloadFileError


class Zone(BaseModel):
    """Class representing zone index data"""

    start: int
    end: int


class Zones(BaseModel):
    """Class representing zone data"""

    introduction: list[Zone] = []
    moyens: list[Zone] = []
    dispositif: list[Zone] = []
    expose: list[Zone] = []
    motivations: list[Zone] = []
    annexes: list[Zone] = []


class File(BaseModel):
    """Class representing file data"""

    id: str
    name: str
    type: JudilibreFileTypeEnum
    isCommunication: bool

    date: str
    size: str | None = None

    url: str
    rawUrl: str | None = None

    def download(
        self,
        filename: str | None = None,
        folder: str = ".",
    ) -> str:
        """Utility function to download a file

        Args:
            filename (str | None, optional): Name of the target file.
                Defaults to None.
            folder (str, optional): Target folder for the file.
                Defaults to ".".

        Raises:
            JudilibreDownloadFileError: raised if the rawUrl is not defined

        Returns:
            str: Path of the target filename
        """
        if self.rawUrl is None:
            raise JudilibreDownloadFileError("rawUrl is not defined")
        with urllib.request.urlopen(self.rawUrl) as web_file:
            content = web_file.read()

        filename = os.path.join(folder, (filename or self.name))

        with open(filename, "wb") as local_file:
            local_file.write(content)

        return filename


class ShortDecision(BaseModel):
    """Class representing decisions in timelines and forward"""

    id: str | None = None
    date: str
    jurisdiction: str | None = None
    chamber: str | None = None
    title: str
    solution: str | None = None
    number: str | None = None


class Article(BaseModel):
    """Class representing an article"""

    title: str


class Legacy(BaseModel):
    """Class representing legacy data"""

    matiereDeterminee: int | None = None
    pourvoiLocal: int | None = None
    pourvoiCcas: int | None = None


class JudilibreShortDecision(BaseModel):
    """Class representing Judilibre Decision data that is common to SearchResult and JudilibreDecision"""

    model_config = ConfigDict(extra="forbid")
    # Mandatory attributes
    ## decision attributes
    id: str
    decision_date: datetime.date
    jurisdiction: JurisdictionEnum | None = None
    number: str
    numbers: list[str]
    publication: list[PublicationCCEnum] | None = None
    solution: SolutionCCEnum | str | None = None  # TODO: remplacer par SolutionEnum
    particularInterest: bool

    # Optional values
    location: LocationCAEnum | LocationTJEnum | LocationTCOMEnum | None = None
    chamber: ChamberCCEnum | str | None = None
    ecli: str | None = None
    formation: FormationCCEnum | None = None  # remplacer par FormationEnum ?
    type: str | None = None
    solution_alt: str | None = None
    summary: str | None = None
    bulletin: str | None = None
    files: list[File] | None = None  # TODO: completer ces schémas
    themes: list | None = None  # TODO: completer ces schémas
    titlesAndSummaries: list[dict] | None = None  # TODO: completer ces schémas

    @field_validator("chamber", mode="before")
    def validate_chamber(cls, v):
        """Validator to enforce ChamberCCEnum"""
        try:
            return ChamberCCEnum(v)
        except ValueError:
            return str(v)

    @field_validator("solution", mode="before")
    def validate_solution(cls, v):
        """Validator to enforce SolutionCCEnum"""
        try:
            return SolutionCCEnum(v)
        except ValueError:
            return str(v)

    def download_all_files(
        self,
        folder: str = ".",
    ) -> list[str]:
        """Utility function to download all the files from this decision

        Args:
            folder (str, optional): Target folder.
                Defaults to ".".

        Returns:
            list[str]: List of filenames
        """
        filenames = []
        if self.files is not None:
            for file in self.files:
                filenames.append(file.download(folder=folder))
        return filenames


class Highlights(BaseModel):
    """Class representing Search Highlights"""

    text: list[str] = []


class JudilibreSearchResult(JudilibreShortDecision):
    """Class representing Search Results"""

    score: float
    highlights: Highlights


class JudilibreDecision(JudilibreShortDecision):
    """Class representing a full Judilibre Decision"""

    source: SourceEnum
    text: str
    update_date: str
    update_datetime: str | None = None
    decision_datetime: str | None = None
    themes: list[str] | None = None
    nac: str | None = None
    portalis: str | None = None
    zones: Zones | None = None
    contested: ShortDecision | None = None
    forward: str | dict | None = None
    timeline: list[ShortDecision] | None = None
    partial: bool | None = None
    visa: list[Article] | None = None
    rapprochements: list[Article] | None = None
    legacy: Legacy | None = None


class JudilibreStatsAggregationKey(BaseModel):
    """Class representing Aggregation Key data"""

    year: int | None = None
    month: str | None = None

    source: SourceEnum | None = None
    jurisdiction: JurisdictionEnum | None = None
    location: LocationCAEnum | LocationTCOMEnum | LocationTJEnum | None = None

    # TODO: Remplacer par des Enums
    chamber: ChamberCCEnum | str | None = None
    formation: FormationCCEnum | None = None
    publication: PublicationCCEnum | None = None
    solution: SolutionCCEnum | str | None = None
    type: str | None = None
    nac: str | None = None
    theme: str | None = None

    @field_validator("chamber", mode="before")
    def validate_chamber(cls, v):
        """Validator to enforce ChamberCCEnum"""
        try:
            return ChamberCCEnum(v)
        except ValueError:
            return str(v)

    @field_validator("solution", mode="before")
    def validate_solution(cls, v):
        """Validator to enforce SolutionCCEnum"""
        try:
            return SolutionCCEnum(v)
        except ValueError:
            return str(v)


class JudilibreAggregatedData(BaseModel):
    """Class representing Aggregation Data results"""

    key: JudilibreStatsAggregationKey
    decisions_count: int


class JudilibreStatsResults(BaseModel):
    """Class representing Aggregation results"""

    min_decision_date: datetime.date | None = None
    max_decision_date: datetime.date | None = None
    total_decisions: int | None = None
    aggregated_data: list[JudilibreAggregatedData] = []


class JudilibreStatsQuery(BaseModel):
    """Class representing STATS query data"""

    date_start: datetime.date | None = None
    date_end: datetime.date | None = None
    jurisdiction: list[JurisdictionEnum] | None = None
    location: list[LocationCAEnum | LocationTJEnum | LocationTCOMEnum] | None = None
    selection: bool | None = None

    keys: list[JudilibreStatsAggregationKeysEnum] | JudilibreStatsAggregationKeysEnum | None = None


class JudilibreStats(BaseModel):
    """Class representing STATS results"""

    results: JudilibreStatsResults
    query: JudilibreStatsQuery


class JudilibreTransaction(BaseModel):
    """Class representing Transaction data"""

    id: str
    action: JudilibreTransactionActionEnum
    date: datetime.datetime
