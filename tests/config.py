import os

from dotenv import load_dotenv
from pyjudilibre import JudilibreClient
from pyjudilibre.enums import (
    JurisdictionEnum,
    LocationCAEnum,
    LocationTJEnum,
    LocationTCOMEnum,
)

load_dotenv()


def get_env_variable(env_variable_name: str) -> str:
    env_variable = os.environ.get(env_variable_name)
    if env_variable is None:
        raise EnvironmentError(f"{env_variable_name} is not set")
    return env_variable.strip()


JUDILIBRE_API_URL = get_env_variable("JUDILIBRE_API_URL")
JUDILIBRE_API_KEY = get_env_variable("JUDILIBRE_API_KEY")

DECISION_CC_ID = "5fca9e9f7fceed9498daf2cf"
DECISION_CA_ID = "649e75f8f84a5e05db33e6af"

client = JudilibreClient(
    judilibre_api_url=JUDILIBRE_API_URL,
    judilibre_api_key=JUDILIBRE_API_KEY,
)

JURISDICTIONS = [
    JurisdictionEnum.cour_de_cassation,
    JurisdictionEnum.cours_d_appel,
    JurisdictionEnum.tribunal_judiciaire,
    JurisdictionEnum.tribunal_de_commerce,
]
LOCATIONS = [
    LocationCAEnum.ca_paris,
    LocationTJEnum.tj_paris,
    LocationTCOMEnum.tae_de_paris,
]
