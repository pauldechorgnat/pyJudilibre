import datetime
from typing import Optional

import requests

from .__version__ import __version__
from .decorators import catch_wrong_url_error
from .exceptions import JudilibreDecisionNotFoundError, JudilibreValueError
from .models.models import JudilibreDecision, SearchResult
from .utils import check_authentication_error, paginate_results


class JudilibreClient:
    """Class that implements a Python Client for the Judilibre API"""

    def __init__(
        self,
        api_url: str,
        api_key_id: str,
    ):
        self.api_url = api_url
        self.api_key_id = api_key_id
        self.__version__ = __version__

        self.api_headers = {
            "KeyId": api_key_id,
            "User-Agent": f"pyJudilibre {self.__version__}",
        }

    @catch_wrong_url_error
    def get(
        self,
        decision_id: str,
    ) -> JudilibreDecision:
        """Returns a decision from Judilibre given its ID

        Args:
            decision_id (str): ID of the decision to look for

        Raises:
            JudilibreDecisionNotFoundError: raised if the ID does not exist

        Returns:
            JudilibreDecision: a decision
        """
        response = requests.get(
            url=f"{self.api_url}/decision?id={decision_id}",
            headers=self.api_headers,
        )

        check_authentication_error(response=response)

        if response.status_code == 404:
            raise JudilibreDecisionNotFoundError(f"Decision with id `{decision_id}` is not found in Judilibre")

        decision = JudilibreDecision(**response.json())

        return decision

    @catch_wrong_url_error
    def healthcheck(self) -> bool:
        """Returns true if the API is up

        Returns:
            bool: True if the API is up, False else
        """
        response = requests.get(
            url=f"{self.api_url}/healthcheck",
            headers=self.api_headers,
        )

        check_authentication_error(response=response)

        if response.json()["status"]:
            return True

        return False

    @catch_wrong_url_error
    def export(
        self,
        max_results: int = 10,
        jurisdictions: list[str] = ["cc", "ca", "tj"],
        date_start: Optional[datetime.date] = None,
        date_end: Optional[datetime.date] = None,
        date_type: str = "creation",  # update
        verbose: bool = False,
        batch_size: int = 10,
        **kwargs,
    ) -> list[JudilibreDecision]:
        """Returns a list of decisions given a query

        Args:
            max_results (int, optional): _description_. Defaults to 10.
            jurisdictions (list[str], optional): _description_. Defaults to ["cc", "ca", "tj"].
            date_start (Optional[datetime.date], optional): _description_. Defaults to None.
            date_end (Optional[datetime.date], optional): _description_. Defaults to None.
            date_type (str, optional): _description_. Defaults to "creation".
            verbose (bool, optional): _description_. Defaults to False.
            batch_size (int, optional): _description_. Defaults to 10.

        Raises:
            JudilibreValueError: _description_

        Returns:
            list[JudilibreDecision]: _description_
        """

        parameters = {}

        if jurisdictions:
            parameters["jurisdiction"] = jurisdictions
        if date_start:
            parameters["date_start"] = date_start
        if date_end:
            parameters["date_end"] = date_end
        if date_type:
            if date_type not in ["creation", "update"]:
                raise JudilibreValueError(f"`date_type` must be 'update' or 'creation' not `{date_type}`")
            parameters["date_type"] = date_type

        # adding more parameters
        parameters = {
            **parameters,
            **kwargs,
        }

        results = paginate_results(
            url=f"{self.api_url}/export",
            headers=self.api_headers,
            parameters=parameters,
            max_results=max_results,
            batch_size=batch_size,
            verbose=verbose,
        )

        return [JudilibreDecision(**r) for r in results]

    @catch_wrong_url_error
    def search(
        self,
        query: str,
        operator: str = "exact",
        jurisdictions: list[str] = ["cc", "ca", "tj"],
        max_results: int = 100,
        page_size: int = 25,
        verbose: bool = False,
        **kwargs,
    ) -> list[JudilibreDecision]:
        """Returns a list of short decisions based on a full text query

        Args:
            query (str): full text query
            operator (str, optional): string that indicates how to look for the query.
                Defaults to "exact".
            jurisdictions (list[str], optional): list of jurisdiction to query for.
                Defaults to ["cc", "ca", "tj"].
            max_results (int, optional): Max number of results from the query.
                Defaults to 100.
            page_size (int, optional): Number of results to return at a time.
                Defaults to 25.
            verbose (bool, optional): If True, will display a progress bar.
                Defaults to False.

        Raises:
            exc: _description_

        Returns:
            list[JudilibreDecision]: _description_
        """
        parameters = {
            "query": query,
            "operator": operator,
            "jurisdiction": jurisdictions,
        }

        parameters = {
            **parameters,
            **kwargs,
        }

        results = paginate_results(
            url=f"{self.api_url}/search",
            headers=self.api_headers,
            parameters=parameters,
            max_results=max_results,
            batch_size=page_size,
            verbose=verbose,
            batch_type="page",
        )

        decisions = []

        for r in results:
            decisions.append(SearchResult(**r))

        return decisions
