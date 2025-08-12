import datetime
import logging
import os

import requests
from httpx import Client
from pyjudilibre.decorators import catch_wrong_url_error
from pyjudilibre.enums import (
    JudilibreTaxonEnum,
    JudilibreStatsAggregationKeysEnum,
    JurisdictionEnum,
    LocationCAEnum,
    LocationTJEnum,
    replace_enums_in_dictionary,
)
from pyjudilibre.exceptions import (
    JudilibreDecisionNotFoundError,
    JudilibreWrongCredentialsError,
    JudilibreResourceNotFoundError,
)
from pyjudilibre.models import (
    JudilibreDecision,
    JudilibreSearchResult,
    JudilibreStats,
)

__version__ = "0.5.6"


def catch_response(response: requests.Response) -> requests.Response:
    if response.status_code == 400:
        message = response.headers.get("WWW-Authenticate", "")
        if message == (
            'Bearer realm="DefaultRealm",error="invalid_request"'
            ',error_description="Unable to find token in the message"'
        ):
            raise JudilibreWrongCredentialsError("Credentials are not valid.")
    if response.status_code == 404:
        raise JudilibreResourceNotFoundError("Resource is not found")
    return response


class JudilibreClient:
    """Class that implements a Python Client for the Judilibre API"""

    def __init__(
        self,
        judilibre_api_url: str | None = None,
        judilibre_api_key: str | None = None,
        logging_level: int = logging.INFO,
    ):
        # HTTP CLIENT
        judilibre_api_url = judilibre_api_url or os.environ["JUDILIBRE_API_URL"]
        judilibre_api_key = judilibre_api_key or os.environ["JUDILIBRE_API_KEY"]

        self.judilibre_api_url = judilibre_api_url
        self.judilibre_api_key = judilibre_api_key
        self.__version__ = __version__

        self.api_headers = {
            "KeyId": self.judilibre_api_key,
            "User-Agent": f"pyJudilibre {self.__version__}",
        }

        self._client = Client(
            base_url=self.judilibre_api_url,
            headers=self.api_headers,
        )

        # LOGGING
        self._logger = logging.getLogger("judilibre-client")
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(level=logging_level)

    @catch_wrong_url_error
    def _query(
        self,
        url: str,
        method: str = "GET",
        params: dict | None = None,
    ) -> requests.Response:
        url = f"{self.judilibre_api_url.rstrip('/')}/{url.lstrip('/')}"

        params = self._clean_params(params)

        self._logger.debug(f"REQUEST METHOD URL:            {method} {url}")
        self._logger.debug(f"REQUEST PARAMETERS: {params}")

        response = self._client.request(
            method=method,
            url=url,
            params=params,
        )

        self._logger.debug(f"RESPONSE STATUS : {response.status_code}")
        self._logger.debug(f"RESPONSE HEADERS: {response.headers}")
        self._logger.debug(f"RESPONSE CONTENT: {response.content.decode('utf-8')}")

        response = catch_response(response=response)  # type: ignore

        return response  # type: ignore

    def decision(
        self,
        decision_id: str,
    ) -> JudilibreDecision:
        params = {
            "id": decision_id,
            "resolve_references": True,
        }
        try:
            response = self._query(
                method="GET",
                url="/decision",
                params=params,
            )
        except JudilibreResourceNotFoundError as exc:
            raise JudilibreDecisionNotFoundError(f"decision with ID {decision_id} not Found") from exc

        return JudilibreDecision(**response.json())

    def healthcheck(
        self,
    ) -> bool:
        """Returns true if the API is up

        Returns:
            bool: True if the API is up, False else
        """
        response = self._query(
            method="GET",
            url="/healthcheck",
        )

        if response.json()["status"]:
            return True

        return False

    def stats(
        self,
        *,
        keys: list[JudilibreStatsAggregationKeysEnum] | None = None,
        location: list[LocationCAEnum | LocationTJEnum] | None = None,
        jurisdictions: list[JurisdictionEnum] | None = None,
        date_start: datetime.date | None = None,
        date_end: datetime.date | None = None,
        selection: bool | None = None,
    ) -> JudilibreStats:
        params = {
            **({"keys": keys} if keys is not None else {}),
            **({"date_start": date_start} if date_start is not None else {}),
            **({"date_end": date_end} if date_end is not None else {}),
            **({"jurisdiction": jurisdictions} if jurisdictions is not None else {}),
            **({"location": location} if location is not None else {}),
            **({"selection": selection} if selection is not None else {}),
        }
        response = self._query(
            method="GET",
            url="/stats",
            params=params,
        )
        return JudilibreStats(**response.json())

    def export(
        self,
        batch_number: int = 0,
        batch_size: int = 10,
        *,
        jurisdictions: list[JurisdictionEnum] | None = None,
        date_start: datetime.date | None = None,
        date_end: datetime.date | None = None,
        date_type: str | None = "creation",
        **kwargs,
    ) -> tuple[int, list[JudilibreDecision]]:
        params = {}

        # adding more parameters
        params = {
            **({"jurisdiction": jurisdictions} if jurisdictions else {}),
            **({"date_start": date_start} if date_start else {}),
            **({"date_end": date_end} if date_end else {}),
            **({"date_type": date_type} if date_type else {}),
            "resolve_references": True,
            "batch": batch_number,
            "batch_size": batch_size,
            **kwargs,
        }

        response = self._query(
            method="GET",
            url="/export",
            params=params,
        )
        response_data = response.json()

        return response_data["total"], [JudilibreDecision(**r) for r in response_data["results"]]

    def search(
        self,
        query: str,
        page_size: int = 25,
        page_number: int = 0,
        *,
        operator: str | None = None,
        date_start: datetime.date | None = None,
        date_end: datetime.date | None = None,
        jurisdictions: list[JurisdictionEnum] | None = None,
        **kwargs,
    ) -> tuple[int, list[JudilibreSearchResult]]:
        params = {
            "query": query,
            "page_size": page_size,
            "page": page_number,
            "resolve_references": True,
            **({"date_start": date_start} if date_start else {}),
            **({"date_end": date_end} if date_end else {}),
            **({"operator": operator} if operator else {}),
            **({"jurisdiction": jurisdictions} if jurisdictions else {}),
            **kwargs,
        }

        response = self._query(
            method="GET",
            url="/search",
            params=params,
        )
        response_data = response.json()

        return response_data["total"], [JudilibreSearchResult(**r) for r in response_data["results"]]

    def search_paginate(
        self,
        query: str,
        max_results: int | None = None,
        *,
        operator: str | None = None,
        date_start: datetime.date | None = None,
        date_end: datetime.date | None = None,
        jurisdictions: list[JurisdictionEnum] | None = None,
        **kwargs,
    ) -> list[JudilibreSearchResult]:
        page_size = 25
        page_number = 0
        next_page = True

        params = {
            "query": query,
            "page_size": page_size,
            "page": page_number,
            "resolve_references": True,
            **({"date_start": date_start} if date_start else {}),
            **({"date_end": date_end} if date_end else {}),
            **({"operator": operator} if operator else {}),
            **({"jurisdiction": jurisdictions} if jurisdictions else {}),
            **kwargs,
        }

        results = []
        n_results = 0

        while next_page:
            print(page_number)
            params["page"] = page_number

            response = self._query(
                method="GET",
                url="/search",
                params=params,
            )

            response_data = response.json()
            new_results = [JudilibreSearchResult(**r) for r in response_data["results"]]
            n_results += len(new_results)

            results.extend(new_results)

            if response_data.get("next_page") is None:
                next_page = False

            if (max_results is not None) and (n_results >= max_results):
                next_page = False

            page_number += 1

        if max_results is not None:
            return results[:max_results]
        return results

    def export_paginate(
        self,
        max_results: int | None = None,
        *,
        jurisdictions: list[JurisdictionEnum] | None = None,
        date_start: datetime.date | None = None,
        date_end: datetime.date | None = None,
        date_type: str | None = "creation",
        **kwargs,
    ) -> list[JudilibreDecision]:
        batch_size = 100
        batch_number = 0
        next_batch = True

        params = {
            "batch_size": batch_size,
            "batch": batch_number,
            "resolve_references": True,
            **({"date_start": date_start} if date_start else {}),
            **({"date_end": date_end} if date_end else {}),
            **({"date_type": date_type} if date_type else {}),
            **({"jurisdiction": jurisdictions} if jurisdictions else {}),
            **kwargs,
        }

        decisions = []
        n_decisions = 0

        while next_batch:
            params["batch"] = batch_number

            response = self._query(
                method="GET",
                url="/export",
                params=params,
            )

            response_data = response.json()
            new_decisions = [JudilibreDecision(**r) for r in response_data["results"]]
            n_decisions += len(new_decisions)

            decisions.extend(new_decisions)

            if response_data.get("next_batch") is None:
                next_batch = False

            if (max_results is not None) and (n_decisions >= max_results):
                next_batch = False

            batch_number += 1

        if max_results is not None:
            return decisions[:max_results]

        return decisions

    @staticmethod
    def _clean_params(params: dict | None) -> dict:
        if params is None:
            return {}
        return replace_enums_in_dictionary(params)  # type: ignore

    def taxonomy(
        self,
        taxon_id: JudilibreTaxonEnum,
        context: JurisdictionEnum,
        *,
        taxon_key: str | None = None,
        taxon_value: str | None = None,
    ) -> dict[str, str]:
        if (taxon_key is not None) and (taxon_value is not None):
            raise ValueError("At least one of taxon_key or taxon_value must be None")

        params = {
            "id": JudilibreTaxonEnum(taxon_id),
            "context_value": JurisdictionEnum(context),
            **({"key": taxon_key} if taxon_key else {}),
            **({"value": taxon_value} if taxon_value else {}),
        }

        response = self._query(
            method="GET",
            url="/taxonomy",
            params=params,
        )
        print(f"{response.status_code=}")
        print(f"{response.content=}")

        response_data = response.json()

        taxons: dict[str, str] = {}

        if taxon_key is not None:
            taxons[taxon_key] = response_data["result"]["value"]
        elif taxon_value is not None:
            taxons[response_data["result"]["key"]] = taxon_value
        else:
            taxons = response_data["result"]

        return taxons
