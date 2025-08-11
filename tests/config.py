import os

from dotenv import load_dotenv

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
