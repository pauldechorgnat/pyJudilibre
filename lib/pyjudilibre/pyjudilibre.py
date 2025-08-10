import datetime
from typing import Optional

import requests
import logging

from pyjudilibre.decorators import catch_wrong_url_error
from pyjudilibre.exceptions import (
    JudilibreValueError,
    JudilibreWrongCredentialsError,
    JudilibreDecisionNotFoundError,
)
from pyjudilibre.models import (
    JudilibreDecision,
    JudilibreSearchResult,
)

from httpx import Client

__version__ = "0.5.0"


def catch_response(response: requests.Response) -> requests.Response:
    if response.status_code == 400:
        message = response.headers.get("WWW-Authenticate", "")
        if message == (
            'Bearer realm="DefaultRealm",error="invalid_request"'
            ',error_description="Unable to find token in the message"'
        ):
            raise JudilibreWrongCredentialsError("Credentials are not valid.")

    return response


class JudilibreClient:
    """Class that implements a Python Client for the Judilibre API"""

    def __init__(
        self,
        judilibre_api_url: str,
        judilibre_api_key: str,
        logging_level: int = logging.INFO,
    ):
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
        print(url)
        response = self._client.request(
            method=method,
            url=url,
            params=params,
        )
        response = catch_response(response=response)  # type: ignore

        self._logger.info(response.request)

        return response  # type: ignore

    def get(
        self,
        decision_id: str,
    ) -> JudilibreDecision:
        response = self._query(
            method="GET",
            url="/decision",
            params={
                "id": decision_id,
                "resolve_references": True,
            },
        )
        if response.status_code == 404:
            raise JudilibreDecisionNotFoundError(f"decision with ID {decision_id} not Found")

        decision = JudilibreDecision(**response.json())

        return decision

    def healthcheck(self) -> bool:
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

    def export(
        self,
        max_results: int = 10,
        jurisdictions: list[str] = ["cc", "ca", "tj"],
        date_start: Optional[datetime.date] = None,
        date_end: Optional[datetime.date] = None,
        date_type: str = "creation",  # update
        batch_size: int = 10,
        **kwargs,
    ) -> list[JudilibreDecision]:
        params = {}

        if jurisdictions:
            params["jurisdiction"] = jurisdictions
        if date_start:
            params["date_start"] = date_start
        if date_end:
            params["date_end"] = date_end
        if date_type:
            if date_type not in ["creation", "update"]:
                raise JudilibreValueError(f"`date_type` must be 'update' or 'creation' not `{date_type}`")
            params["date_type"] = date_type

        # adding more parameters
        params = {
            "resolve_references": True,
            **params,
            **kwargs,
        }

        results = self._paginate_results(
            url="/export",
            params=params,
            max_results=max_results,
            batch_size=batch_size,
            batch_type="batch",
        )

        return [JudilibreDecision(**r) for r in results]

    def search(
        self,
        query: str,
        operator: str = "exact",
        jurisdictions: list[str] = ["cc", "ca", "tj"],
        max_results: int = 100,
        page_size: int = 25,
        **kwargs,
    ) -> list[JudilibreDecision]:
        params = {
            "query": query,
            "operator": operator,
            "jurisdiction": jurisdictions,
            "resolve_references": True,
        }

        params = {
            **params,
            **kwargs,
        }

        results = self._paginate_results(
            url="/search",
            params=params,
            max_results=max_results,
            batch_size=page_size,
            batch_type="page",
        )

        decisions = []

        for r in results:
            decisions.append(JudilibreSearchResult(**r))

        return decisions

    def stats(
        self,
        keys: list[str] = [],  # month, year,
        date_start: datetime.date | None = None,
        date_end: datetime.date | None = None,
        jurisdiction: str | None = None,
        location: list[str] | None = None,
        selection: bool | None = None,
    ) -> list:  # TODO: changer ça
        params = {
            **({"keys": keys} if keys is not None else {}),
            **({"date_start": date_start} if date_start is not None else {}),
            **({"date_end": date_end} if date_end is not None else {}),
            **({"jurisdiction": jurisdiction} if jurisdiction is not None else {}),
            **({"location": location} if location is not None else {}),
            **({"selection": selection} if selection is not None else {}),
        }
        response = self._query(
            method="GET",
            url="/stats",
            params=params,
        )

        data = response.json()

        return data["results"]

    def _paginate_results(
        self,
        url: str,
        method: str = "GET",
        params: dict = {},
        batch_size: int = 10,
        max_results: int = 10_000,
        batch_type: str = "batch",
    ) -> list[dict]:
        # checking batch parameters
        if batch_size > 1_000:
            raise JudilibreValueError(f"'{batch_type}' parameter cannot be more than 1,000.")
        elif batch_size < 1:
            raise JudilibreValueError(f"'{batch_type}' parameter cannot be less than 1.")

        if max_results > 10_000:
            raise JudilibreValueError("Judilibre cannot return more than 10,000 results for a given query.")
        elif max_results < 1:
            raise JudilibreValueError("'max_results' cannot be less than 1.")

        if max_results < batch_size:
            batch_size = max_results

        params[f"{batch_type}_size"] = batch_size

        n_batches = (max_results // batch_size) + 1
        remaining_results = max_results % batch_size

        decisions = []
        n_decisions = 0

        batch_numbers = range(n_batches)

        for index_batch in batch_numbers:
            params[batch_type] = index_batch

            response = self._query(
                method=method,
                url=url,
                params=params,
            )

            data = response.json()

            if "results" in data:
                if index_batch != n_batches - 1:
                    decisions.extend(data["results"])
                    n_decisions += batch_size
                else:
                    decisions.extend(data["results"][:remaining_results])
                    n_decisions += remaining_results

            else:
                break

            if data.get(f"next_{batch_type}") is None:
                break

        return decisions
