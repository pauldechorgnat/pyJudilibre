import datetime
import os
import urllib.request

from pydantic import BaseModel, ConfigDict, field_validator

from pyjudilibre.enums import (
    ChamberCCEnum,
    FormationCCEnum,
    JudilibreDateTypeEnum,
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
    ZoneTypeEnum,
)
from pyjudilibre.exceptions import JudilibreDownloadFileError


class Zone(BaseModel):
    """Class representing zone index data"""

    model_config = ConfigDict(extra="forbid")

    start: int
    end: int | None


class ZoneWithText(Zone):
    text: str
    type: ZoneTypeEnum


class Zones(BaseModel):
    """Class representing zone data"""

    model_config = ConfigDict(extra="forbid")

    introduction: list[Zone] = []
    moyens: list[Zone] = []
    dispositif: list[Zone] = []
    expose: list[Zone] = []
    motivations: list[Zone] = []
    annexes: list[Zone] = []


class Zoning:
    def __init__(
        self,
        text: str,
        zones: Zones | None,
    ):
        self.text = text
        all_zones: list[ZoneWithText] = []

        if zones is not None:
            _all_zones = [
                *[self._get_zone_with_text(z, type=ZoneTypeEnum.introduction) for z in zones.introduction],
                *[self._get_zone_with_text(z, type=ZoneTypeEnum.expose_du_litige) for z in zones.expose],
                *[self._get_zone_with_text(z, type=ZoneTypeEnum.moyen) for z in zones.moyens],
                *[self._get_zone_with_text(z, type=ZoneTypeEnum.motivation) for z in zones.motivations],
                *[self._get_zone_with_text(z, type=ZoneTypeEnum.dispositif) for z in zones.dispositif],
                *[self._get_zone_with_text(z, type=ZoneTypeEnum.moyen_annexe) for z in zones.annexes],
            ]

            all_zones = sorted(
                [z for z in _all_zones if z is not None],
                key=lambda zone: zone.start,
            )

        self.all: list[ZoneWithText] = all_zones

        self.introduction = self._get_unique_zone(
            list(
                filter(
                    lambda zone: zone.type == ZoneTypeEnum.introduction,
                    all_zones,
                ),
            )
        )
        self.expose_du_litige = self._get_unique_zone(
            list(
                filter(
                    lambda zone: zone.type == ZoneTypeEnum.expose_du_litige,
                    all_zones,
                ),
            )
        )
        self.dispositif = self._get_unique_zone(
            list(
                filter(
                    lambda zone: zone.type == ZoneTypeEnum.dispositif,
                    all_zones,
                ),
            )
        )

        self.moyens = list(
            filter(
                lambda zone: zone.type == ZoneTypeEnum.moyen,
                all_zones,
            ),
        )

        self.motivations = list(
            filter(
                lambda zone: zone.type == ZoneTypeEnum.motivation,
                all_zones,
            ),
        )

        self.moyens_annexes = list(
            filter(
                lambda zone: zone.type == ZoneTypeEnum.moyen_annexe,
                all_zones,
            ),
        )

    def _get_zone_with_text(
        self,
        zone: Zone | None,
        type: ZoneTypeEnum,
    ) -> ZoneWithText | None:
        if zone is None:
            return None
        return ZoneWithText(
            start=zone.start,
            end=zone.end,
            text=self.text[zone.start : zone.end],
            type=type,
        )

    def _get_unique_zone(
        self,
        zones: list[ZoneWithText],
    ) -> ZoneWithText | None:
        if len(zones) == 0:
            return None
        else:
            return zones[0]


class File(BaseModel):
    """Class representing file data"""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    type: JudilibreFileTypeEnum
    isCommunication: bool
    isAttache: bool | None = None
    isPreparatoire: bool | None = None

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

    model_config = ConfigDict(extra="forbid")

    id: str | None = None
    date: str
    jurisdiction: str | None = None
    chamber: str | int | None = None
    title: str
    solution: str | None = None
    number: str | None = None


class Article(BaseModel):
    """Class representing an article"""

    title: str


class Legacy(BaseModel):
    """Class representing legacy data"""

    model_config = ConfigDict(extra="forbid")

    matiereDeterminee: int | None = None
    pourvoiLocal: int | None = None
    pourvoiCcas: int | None = None
    selection: int | None = None


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

    # Other
    decision_datetime: str | None = None
    nac: str | None = None
    portalis: str | None = None

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
    model_config = ConfigDict(extra="forbid")
    """Class representing Search Highlights"""

    text: list[str] = []


class JudilibreSearchResult(JudilibreShortDecision):
    model_config = ConfigDict(extra="forbid")
    """Class representing Search Results"""

    score: float
    highlights: Highlights


class JudilibreDecision(JudilibreShortDecision):
    model_config = ConfigDict(extra="forbid")
    """Class representing a full Judilibre Decision"""

    source: SourceEnum
    text: str
    update_date: str
    update_datetime: str | None = None
    # decision_datetime: str | None = None
    themes: list[str] | None = None
    # nac: str | None = None
    # portalis: str | None = None
    zones: Zones | None = None
    contested: ShortDecision | None = None
    forward: str | dict | None = None
    timeline: list[ShortDecision] | None = None
    partial: bool | None = None
    visa: list[Article] | None = None
    rapprochements: list[Article] | None = None
    legacy: Legacy | None = None

    @property
    def zoning(self):
        return Zoning(text=self.text, zones=self.zones)


class JudilibreStatsAggregationKey(BaseModel):
    """Class representing Aggregation Key data"""

    model_config = ConfigDict(extra="forbid")

    year: int | None = None
    month: str | None = None

    source: SourceEnum | None = None
    jurisdiction: JurisdictionEnum | None = None
    location: LocationCAEnum | LocationTCOMEnum | LocationTJEnum | None = None
    particularInterest: bool | None = None

    # TODO: Remplacer par des Enums
    chamber: ChamberCCEnum | str | None = None
    formation: FormationCCEnum | None = None
    publication: PublicationCCEnum | None = None
    solution: SolutionCCEnum | str | None = None
    type: str | None = None
    nac: str | None = None
    theme: str | None = None

    filetype: JudilibreFileTypeEnum | None = None

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

    model_config = ConfigDict(extra="forbid")

    key: JudilibreStatsAggregationKey
    decisions_count: int


class JudilibreStatsResults(BaseModel):
    """Class representing Aggregation results"""

    model_config = ConfigDict(extra="forbid")

    min_decision_date: datetime.date | None = None
    max_decision_date: datetime.date | None = None
    total_decisions: int | None = None
    aggregated_data: list[JudilibreAggregatedData] = []


class JudilibreStatsQuery(BaseModel):
    """Class representing STATS query data"""

    model_config = ConfigDict(extra="forbid")

    date_start: datetime.date | None = None
    date_end: datetime.date | None = None
    date_type: JudilibreDateTypeEnum | None = None
    jurisdiction: list[JurisdictionEnum] | None = None
    location: list[LocationCAEnum | LocationTJEnum | LocationTCOMEnum] | None = None
    particularInterest: bool | None = None

    keys: list[JudilibreStatsAggregationKeysEnum] | JudilibreStatsAggregationKeysEnum | None = None


class JudilibreStats(BaseModel):
    """Class representing STATS results"""

    model_config = ConfigDict(extra="forbid")

    results: JudilibreStatsResults
    query: JudilibreStatsQuery


class JudilibreTransaction(BaseModel):
    """Class representing Transaction data"""

    model_config = ConfigDict(extra="forbid")

    id: str
    action: JudilibreTransactionActionEnum
    date: datetime.datetime


test_decision_data = dict(
    id="1234",
    jurisdiction="cc",
    text="",
    number="1234",
    numbers=["1234"],
    particularInterest=True,
    source="jurinet",
    update_date=str(datetime.datetime.now()),
    decision_date=str(datetime.date.today()),
)
