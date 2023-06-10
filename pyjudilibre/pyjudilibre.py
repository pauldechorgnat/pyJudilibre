import requests

from .exceptions import (
    JudilibreDecisionNotFoundError,
    JudilibreWrongCredentialsError,
    JudilibreWrongURLError,
)
from .models import JudilibreDecision
from .references import (
    CA_DECISION_TYPES,
    CA_LOCATIONS,
    CA_THEMES,
    CC_CHAMBERS,
    CC_DECISION_TYPES,
    CC_FORMATIONS,
    CC_PUBLICATIONS,
    CC_SOLUTIONS,
    CC_THEMES,
)


class JudilibreClient:
    """Class that implements a Python Client for the Judilibre API"""

    def __init__(self, api_url: str, api_key_id: str, action_on_check: str = "warning"):
        self.api_url = api_url
        self.api_key_id = api_key_id
        self.__version__ = "0.0.1"
        self.action_on_check = action_on_check

        self.cc_decision_type_values = CC_DECISION_TYPES
        self.cc_decision_solution_values = CC_SOLUTIONS
        self.cc_chamber_values = CC_CHAMBERS
        self.cc_formation_values = CC_FORMATIONS
        self.cc_mateer = CC_THEMES
        self.cc_publication = CC_PUBLICATIONS

        self.ca_decision_type_values = CA_DECISION_TYPES
        self.ca_nac = CA_THEMES
        self.ca_locations = CA_LOCATIONS

        self.api_headers = {
            "KeyId": api_key_id,
            "User-Agent": f"pyJudilibre {self.__version__}",
        }

    def search(self):
        pass

    def export(self):
        pass

    def get(self, decision_id: str) -> JudilibreDecision:
        try:
            response = requests.get(
                url=f"{self.api_url}/decision?id={decision_id}",
                headers=self.api_headers,
            )
        except requests.exceptions.ConnectionError as exc:
            raise JudilibreWrongURLError(
                f"URL `{self.api_url}` is not reachable."
            ) from exc
        if response.status_code == 400:
            raise JudilibreWrongCredentialsError("Credentials are not valid.")
        elif response.status_code == 404:
            raise JudilibreDecisionNotFoundError(
                f"Decision with id `{decision_id}` is not found in Judilibre"
            )
        decision = JudilibreDecision(**response.json())

        return decision

    def healthcheck(self):
        try:
            response = requests.get(
                url=f"{self.api_url}/healthcheck", headers=self.api_headers
            )

        except requests.exceptions.ConnectionError as exc:
            raise JudilibreWrongURLError(
                f"URL `{self.api_url}` is not reachable."
            ) from exc

        if response.status_code != 200:
            raise JudilibreWrongCredentialsError("Credentials are not valid.")

        if response.json()["status"]:
            return True

        return False
