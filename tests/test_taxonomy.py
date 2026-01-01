import pytest
from pyjudilibre.enums import (
    JudilibreTaxonEnum,
    JurisdictionEnum,
    LocationCAEnum,
)
from pyjudilibre.exceptions import JudilibreResourceNotFoundError

from .config import client


def test_taxonomy_ca_locations():
    computed_taxons = client.taxonomy(
        taxon_id=JudilibreTaxonEnum.location,
        context=JurisdictionEnum.cours_d_appel,
    )

    for key, value in computed_taxons.items():
        assert LocationCAEnum(key)._all_values == (value, key)  # type: ignore
        assert LocationCAEnum(value)._all_values == (value, key)  # type: ignore


def test_taxonomy_ca_locations_with_taxon_key():
    computed_taxons = client.taxonomy(
        taxon_id=JudilibreTaxonEnum.location,
        context=JurisdictionEnum.cours_d_appel,
        taxon_key="ca_agen",
    )

    expected_taxons = {"ca_agen": "Cour d'appel d'Agen"}

    assert expected_taxons == computed_taxons


def test_taxonomy_ca_locations_with_taxon_value():
    computed_taxons = client.taxonomy(
        taxon_id=JudilibreTaxonEnum.location,
        context=JurisdictionEnum.cours_d_appel,
        taxon_value="Cour d'appel d'Agen",
    )

    expected_taxons = {"ca_agen": "Cour d'appel d'Agen"}

    assert expected_taxons == computed_taxons


def test_taxonomy_wrong_taxon_id():
    with pytest.raises(ValueError):
        client.taxonomy(
            taxon_id="obviously_wrong_taxon_id",  # type: ignore
            context=JurisdictionEnum.cours_d_appel,
        )


def test_taxonomy_wrong_taxon_key():
    with pytest.raises(JudilibreResourceNotFoundError):
        client.taxonomy(
            taxon_id=JudilibreTaxonEnum.location,
            context=JurisdictionEnum.cours_d_appel,
            taxon_key="obviously_wrong_taxon_key",
        )


def test_taxonomy_wrong_taxon_value():
    with pytest.raises(JudilibreResourceNotFoundError):
        client.taxonomy(
            taxon_id=JudilibreTaxonEnum.location,
            context=JurisdictionEnum.cours_d_appel,
            taxon_value="obviously_wrong_taxon_value",
        )
