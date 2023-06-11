from typing import Union

import requests

from .decorators import catch_wrong_url_error
from .exceptions import JudilibreDecisionNotFoundError
from .models import JudilibreDecision
from .references import (
    CA_DECISION_TYPES,
    CA_LOCATIONS,
    CA_SOLUTIONS,
    CA_THEMES,
    CC_CHAMBERS,
    CC_DECISION_TYPES,
    CC_FORMATIONS,
    CC_PUBLICATIONS,
    CC_SOLUTIONS,
    CC_THEMES,
)
from .utils import check_authentication_error, check_date, check_value, paginate_results


class JudilibreClient:
    """Class that implements a Python Client for the Judilibre API"""

    def __init__(self, api_url: str, api_key_id: str, action_on_check: str = "warning"):
        self.api_url = api_url
        self.api_key_id = api_key_id
        self.__version__ = "0.0.1"
        self.action_on_check = action_on_check

        self.cc_decision_type_values: dict = CC_DECISION_TYPES
        self.cc_solution_values: dict = CC_SOLUTIONS
        self.cc_chamber_values: dict = CC_CHAMBERS
        self.cc_formation_values: dict = CC_FORMATIONS
        self.cc_theme_values: set = CC_THEMES
        self.cc_publication: dict = CC_PUBLICATIONS

        self.ca_decision_type_values: dict = CA_DECISION_TYPES
        self.ca_nac_values: dict = CA_THEMES
        self.ca_location_values: dict = CA_LOCATIONS
        self.ca_solution_values: dict = CA_SOLUTIONS

        self.all_decision_type_values: dict = {**CC_DECISION_TYPES, **CA_DECISION_TYPES}
        self.all_solution_values: dict = {**CC_SOLUTIONS, **CA_SOLUTIONS}
        self.all_theme_values: set = CC_THEMES.update(CA_THEMES)

        self.api_headers = {
            "KeyId": api_key_id,
            "User-Agent": f"pyJudilibre {self.__version__}",
        }

    def _check_ca_parameters(
        self,
        parameters: dict[str, list[str]] = {},
        action_on_check: str = "raise",
    ) -> bool:
        checks = []

        for parameter in parameters:
            checks.append(
                check_value(
                    value=parameter,
                    allowed_values=[
                        "location",
                        "theme",
                        "type",
                        "jurisdiction",
                        "solution",
                    ],
                    message="{value} is not a valid parameters for CA context.",
                    action_on_check=action_on_check,
                )
            )
        if "location" in parameters:
            for location in parameters["location"]:
                checks.append(
                    check_value(
                        value=location,
                        allowed_values=self.ca_location_values,
                        value_name="location",
                        action_on_check=action_on_check,
                    )
                )
        if "theme" in parameters:
            for nac in parameters["theme"]:
                checks.append(
                    check_value(
                        value=nac,
                        allowed_values=self.ca_nac_values,
                        value_name="nac",
                        action_on_check=action_on_check,
                    )
                )
        if "type" in parameters:
            for decision_type in parameters["type"]:
                checks.append(
                    check_value(
                        value=decision_type,
                        allowed_values=self.ca_decision_type_values,
                        value_name="decision_type",
                        action_on_check=action_on_check,
                    )
                )

        if "solution" in parameters:
            for solution in parameters["solution"]:
                checks.append(
                    check_value(
                        value=solution,
                        allowed_values=self.ca_solution_values,
                        value_name="solution",
                        action_on_check=action_on_check,
                    )
                )

        return all(checks)

    def _check_cc_parameters(
        self, parameters: dict, action_on_check: str = "raise"
    ) -> bool:
        checks = []

        for parameter in parameters:
            checks.append(
                check_value(
                    value=parameter,
                    allowed_values=[
                        "theme",
                        "type",
                        "jurisdiction",
                        "solution",
                        "chamber",
                        "formation",
                        "publication",
                    ],
                    message="{value} is not a valid parameters for CC context.",
                    action_on_check=action_on_check,
                )
            )
        if "solution" in parameters:
            for solution in parameters["solution"]:
                checks.append(
                    check_value(
                        value=solution,
                        allowed_values=self.cc_decision_solution_values,
                        value_name="solution",
                        action_on_check=action_on_check,
                    )
                )

        if "type" in parameters:
            for decision_type in parameters["type"]:
                checks.append(
                    check_value(
                        value=decision_type,
                        allowed_values=self.cc_decision_type_values,
                        value_name="decision_type",
                        action_on_check=action_on_check,
                    )
                )
        if "theme" in parameters:
            for theme in parameters["theme"]:
                checks.append(
                    check_value(
                        value=theme,
                        allowed_values=self.cc_theme_values,
                        value_name="theme",
                        action_on_check=action_on_check,
                    )
                )
        if "chamber" in parameters:
            for chamber in parameters["chamber"]:
                checks.append(
                    check_value(
                        value=chamber,
                        allowed_values=self.cc_chamber_values,
                        value_name="chamber",
                        action_on_check=action_on_check,
                    )
                )

        if "formation" in parameters:
            for formation in parameters["formation"]:
                checks.append(
                    check_value(
                        value=formation,
                        allowed_values=self.cc_formation_values,
                        value_name="formation",
                        action_on_check=action_on_check,
                    )
                )

        if "publication" in parameters:
            for publication in parameters["publication"]:
                checks.append(
                    check_value(
                        value=publication,
                        allowed_values=self.cc_publication,
                        value_name="publication",
                        action_on_check=action_on_check,
                    )
                )

        return all(checks)

    def _check_all_parameters(self, parameters: dict, action_on_check: str = "raise"):
        checks = []

        for parameter in parameters:
            checks.append(
                check_value(
                    value=parameter,
                    allowed_values=[
                        "theme",
                        "type",
                        "jurisdiction",
                        "solution",
                        "chamber",
                        "formation",
                        "publication",
                        "location",
                    ],
                    message="{value} is not a valid parameters for CC context.",
                    action_on_check=action_on_check,
                )
            )

        if "location" in parameters:
            for location in parameters["location"]:
                checks.append(
                    check_value(
                        value=location,
                        allowed_values=self.ca_location_values,
                        value_name="location",
                        action_on_check=action_on_check,
                    )
                )
        if "solution" in parameters:
            for solution in parameters["solution"]:
                checks.append(
                    check_value(
                        value=solution,
                        allowed_values=self.all_solution_values,
                        value_name="solution",
                        action_on_check=action_on_check,
                    )
                )

        if "type" in parameters:
            for decision_type in parameters["type"]:
                checks.append(
                    check_value(
                        value=decision_type,
                        allowed_values=self.all_decision_type_values,
                        value_name="decision_type",
                        action_on_check=action_on_check,
                    )
                )
        if "theme" in parameters:
            for theme in parameters["theme"]:
                checks.append(
                    check_value(
                        value=theme,
                        allowed_values=self.all_theme_values,
                        value_name="theme",
                        action_on_check=action_on_check,
                    )
                )
        if "chamber" in parameters:
            for chamber in parameters["chamber"]:
                checks.append(
                    check_value(
                        value=chamber,
                        allowed_values=self.cc_chamber_values,
                        value_name="chamber",
                        action_on_check=action_on_check,
                    )
                )

        if "formation" in parameters:
            for formation in parameters["formation"]:
                checks.append(
                    check_value(
                        value=formation,
                        allowed_values=self.cc_formation_values,
                        value_name="formation",
                        action_on_check=action_on_check,
                    )
                )

        if "publication" in parameters:
            for publication in parameters["publication"]:
                checks.append(
                    check_value(
                        value=publication,
                        allowed_values=self.cc_publication,
                        value_name="publication",
                        action_on_check=action_on_check,
                    )
                )

        return all(checks)

    def search(self):
        pass

    def export(
        self,
        max_results: int = 10,
        juridisctions: list[str] = ["cc"],
        decision_types: list[str] = [],
        decision_themes: list[str] = [],
        chambers: list[str] = [],
        formations: list[str] = [],
        locations: list[str] = [],
        publications: list[str] = [],
        solutions: list[str] = [],
        date_start: Union[str, None] = None,
        date_end: Union[str, None] = None,
        date_type: str = "creation",  # update
        order: str = "asc",  # desc,
        verbose: bool = False,
        batch_size: int = 10,
        action_on_check: Union[str, None] = None,
    ):
        action_on_check = (
            action_on_check if action_on_check is not None else self.action_on_check
        )

        parameters = {}

        if juridisctions:
            parameters["jurisdiction"] = juridisctions

        if decision_types:
            parameters["type"] = decision_types

        if decision_themes:
            parameters["theme"] = decision_themes

        if chambers:
            parameters["chamber"] = chambers

        if formations:
            parameters["formation"] = formations

        if locations:
            parameters["location"] = locations

        if publications:
            parameters["publication"] = publications

        if solutions:
            parameters["solution"] = solutions

        for jurisdiction_value in juridisctions:
            check_value(
                value=jurisdiction_value,
                value_name="jurisdiction",
                allowed_values=["cc", "ca"],
                action_on_check=action_on_check,
            )

        if juridisctions == ["ca"]:
            self._check_ca_parameters(
                parameters=parameters, action_on_check=action_on_check
            )
        elif juridisctions == ["cc"]:
            self._check_cc_parameters(
                parameters=parameters, action_on_check=action_on_check
            )

        if date_start is not None:
            check_date(date_start, action_on_check=action_on_check)
            parameters["date_start"] = date_start

        if date_end is not None:
            check_date(date_end, action_on_check=action_on_check)
            parameters["date_end"] = date_end
        if date_type:
            check_value(
                value=date_type,
                allowed_values=["creation", "update"],
                value_name="date_type",
                action_on_check=action_on_check,
            )
            parameters["date_type"] = date_type

        if order:
            check_value(
                value=order,
                allowed_values=["desc", "asc"],
                value_name="order",
                action_on_check=action_on_check,
            )

            parameters["order"] = order

        results = paginate_results(
            url=f"{self.api_url}/export",
            headers=self.api_headers,
            params=parameters,
            max_results=max_results,
            batch_size=batch_size,
            verbose=verbose,
        )

        return [JudilibreDecision(**d) for d in results]

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
