import pytest

from pyjudilibre.enums import (
    ChamberCCEnum,
    DecisionTypeCAEnum,
    DecisionTypeCCEnum,
    FormationCCEnum,
    JudilibreDateTypeEnum,
    JudilibreFieldEnum,
    JudilibreFileTypeEnum,
    JudilibreMultiValueEnum,
    JudilibreOperatorEnum,
    JudilibreOrderEnum,
    JudilibreSortEnum,
    JudilibreTaxonEnum,
    JurisdictionEnum,
    LocationCAEnum,
    LocationTCOMEnum,
    LocationTJEnum,
    PublicationCCEnum,
    SolutionCCEnum,
)

from .config import client

PARAMETERS = [
    # LOCATIONS
    (JudilibreTaxonEnum.location, JurisdictionEnum.cours_d_appel, LocationCAEnum),
    # (JudilibreTaxonEnum.location, JurisdictionEnum.tribunaux_judiciaires, LocationTJEnum), skipped
    (JudilibreTaxonEnum.location, JurisdictionEnum.tribunaux_de_commerce, LocationTCOMEnum),
    # TECHNICAL FIELDS
    (JudilibreTaxonEnum.date_type, JurisdictionEnum.cour_de_cassation, JudilibreDateTypeEnum),
    (JudilibreTaxonEnum.query_operator, JurisdictionEnum.cour_de_cassation, JudilibreOperatorEnum),
    (JudilibreTaxonEnum.file_type, JurisdictionEnum.cour_de_cassation, JudilibreFileTypeEnum),
    (JudilibreTaxonEnum.text_query_field, JurisdictionEnum.cour_de_cassation, JudilibreFieldEnum),
    (JudilibreTaxonEnum.sort_variable, JurisdictionEnum.cour_de_cassation, JudilibreSortEnum),
    (JudilibreTaxonEnum.sort_order, JurisdictionEnum.cour_de_cassation, JudilibreOrderEnum),
    # COUR DE CASSATION FIELDS
    (JudilibreTaxonEnum.publication, JurisdictionEnum.cour_de_cassation, PublicationCCEnum),
    (JudilibreTaxonEnum.decision_type, JurisdictionEnum.cour_de_cassation, DecisionTypeCCEnum),
    (JudilibreTaxonEnum.formation, JurisdictionEnum.cour_de_cassation, FormationCCEnum),
    (JudilibreTaxonEnum.chamber, JurisdictionEnum.cour_de_cassation, ChamberCCEnum),
    (JudilibreTaxonEnum.solution, JurisdictionEnum.cour_de_cassation, SolutionCCEnum),
    # COURS D'APPEL FIELDS
    (JudilibreTaxonEnum.decision_type, JurisdictionEnum.cours_d_appel, DecisionTypeCAEnum),
]


@pytest.mark.parametrize("taxon_id,context,enum", PARAMETERS)
def test_check_taxons(
    taxon_id: JudilibreTaxonEnum,
    context: JurisdictionEnum,
    enum: JudilibreMultiValueEnum,
):
    computed_taxons = client.taxonomy(
        taxon_id=taxon_id,
        context=context,
    )

    for key, value in computed_taxons.items():
        assert (enum(key)._all_values[0], enum(key)._all_values[-1]) == (value, key)  # type: ignore
        assert (enum(value)._all_values[0], enum(value)._all_values[-1]) == (value, key)  # type: ignore

    for e in enum:  # type: ignore
        assert e._all_values[-1] in computed_taxons


CITY_NAMES_PARAMETERS = [
    (LocationCAEnum.ca_agen, "Agen"),
    (LocationCAEnum.ca_paris, "Paris"),
    (LocationTJEnum.tj_paris, "Paris"),
    (LocationTJEnum.tj_agen, "Agen"),
    (LocationTJEnum.tj_sables_d_olonne, "Les Sables-d'Olonne"),
    (LocationTJEnum.tj_mans, "Le Mans"),
    (LocationTCOMEnum.tae_de_paris, "Paris"),
    (LocationTCOMEnum.tae_d_avignon, "Avignon"),
    (LocationTCOMEnum.tae_du_mans, "Le Mans"),
    (LocationTCOMEnum.tcom_puy_en_velay, "Le Puy-en-Velay"),
    (LocationTCOMEnum.tcom_rennes, "Rennes"),
    (LocationTCOMEnum.tcom_agen, "Agen"),
]


@pytest.mark.parametrize(
    "location, city_name",
    CITY_NAMES_PARAMETERS,
)
def test_city_names(location, city_name):
    assert location.city == city_name
