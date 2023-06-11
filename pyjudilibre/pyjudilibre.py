from typing import Union

import requests

from .decorators import catch_wrong_url_error
from .exceptions import JudilibreDecisionNotFoundError
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
from .utils import check_authentication_error, check_value


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

    def export(
        self,
        n_results: int = 10,
        juridisction: list[str] = ["cc"],
        decision_type: list[str] = [],
        decision_theme: list[str] = [],
        chamber: list[str] = [],
        formation: list[str] = [],
        # commitee:list[str]=[],
        publication: list[str] = [],
        solution: list[str] = [],
        date_start: Union[str, None] = None,
        date_end: Union[str, None] = None,
        date_type: str = "creation",  # update
        order: str = "asc",  # desc,
        action_on_check: Union[str, None] = None,
    ):
        action_on_check = (
            action_on_check if action_on_check is not None else self.action_on_check
        )
        parameters = {}

        if len(juridisction) > 0:
            for jurisdiction_value in juridisction:
                check_value(
                    value=jurisdiction_value,
                    value_name="jurisdiction",
                    allowed_values=["cc", "ca"],
                    action_on_check=action_on_check,
                )
            parameters["jurisdiction"] = juridisction

        if len(decision_type) > 0:
            for type_value in decision_type:
                check_value(
                    value=type_value,
                    value_name="decision_type",
                    allowed_values=self.cc_decision_type_values,
                )

    @catch_wrong_url_error
    def get(self, decision_id: str) -> JudilibreDecision:
        response = requests.get(
            url=f"{self.api_url}/decision?id={decision_id}",
            headers=self.api_headers,
        )

        check_authentication_error(status_code=response.status_code)

        if response.status_code == 404:
            raise JudilibreDecisionNotFoundError(
                f"Decision with id `{decision_id}` is not found in Judilibre"
            )
        decision = JudilibreDecision(**response.json())

        return decision

    @catch_wrong_url_error
    def healthcheck(self):
        response = requests.get(
            url=f"{self.api_url}/healthcheck", headers=self.api_headers
        )

        check_authentication_error(status_code=response.status_code)

        if response.json()["status"]:
            return True

        return False
