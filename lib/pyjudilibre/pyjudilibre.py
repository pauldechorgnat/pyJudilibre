import datetime
import logging
import os
from urllib.parse import parse_qs

from httpx import Client, Response
from tqdm import tqdm

from pyjudilibre.decorators import catch_wrong_url_error
from pyjudilibre.enums import (
    JudilibreDateTypeEnum,
    JudilibreOperatorEnum,
    JudilibreStatsAggregationKeysEnum,
    JudilibreTaxonEnum,
    JurisdictionEnum,
    LocationCAEnum,
    LocationTCOMEnum,
    LocationTJEnum,
    replace_enums_in_dictionary,
)
from pyjudilibre.exceptions import (
    JudilibreDecisionNotFoundError,
    JudilibreResourceNotFoundError,
    JudilibreWrongCredentialsError,
)
from pyjudilibre.models import (
    JudilibreDecision,
    JudilibreSearchResult,
    JudilibreShortDecision,
    JudilibreStats,
    JudilibreTransaction,
)

__version__ = "0.11.0"


def catch_response(response: Response) -> Response:
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
    """Class that implements a Python Client for the **JUDILIBRE** API"""

    def __init__(
        self,
        judilibre_api_key: str | None = None,
        judilibre_api_url: str | None = None,
        judilibre_api_headers: dict = {},
        proxy: str | None = None,
        logging_level: int = logging.ERROR,
    ):
        """Constructor of the `JudilibreClient` class

        Args:
            judilibre_api_key (str | None, optional): **JUDILIBRE** API key retrieved from [PISTE](https://piste.gouv.fr).
                If `None`, `pyjudilibre` will try to use the `JUDILIBRE_API_KEY` environment variable.
                Defaults to None.
            judilibre_api_url (_type_, optional): JUDLIBRE API URL.
                If `None`, `pyjudilibre` will try to use the `JUDILIBRE_API_URL` environment variable.
                Defaults to None.
            logging_level (int, optional): Level of logs that you want to get from `JudilibreClient`.
                Defaults to logging.INFO.
        """
        # HTTP CLIENT
        judilibre_api_url = judilibre_api_url or os.environ["JUDILIBRE_API_URL"]
        judilibre_api_key = judilibre_api_key or os.environ["JUDILIBRE_API_KEY"]

        self.judilibre_api_url = judilibre_api_url
        self.judilibre_api_key = judilibre_api_key
        self.judilibre_api_headers = judilibre_api_headers
        self.proxy = proxy
        self.__version__ = __version__

        self.api_headers = {
            **judilibre_api_headers,
            "KeyId": self.judilibre_api_key,
            "User-Agent": f"pyJudilibre {self.__version__}",
        }

        self._client = Client(
            base_url=self.judilibre_api_url,
            headers=self.api_headers,
            proxy=proxy,
        )

        # LOGGING
        self._logger = logging.getLogger("judilibre-client")
        if len(self._logger.handlers) == 0:
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
        timeout: int | None = 5,
    ) -> Response:
        """Internal method to query the **JUDILIBRE** API constistently trhoughout methods.

        Args:
            url (str): URL endpoint to query (for example "/search", "/export")
            method (str, optional): HTTP method to use for the query.
                Defaults to "GET".
            params (dict | None, optional): query string parameters.
                Defaults to None.
            timeout (int | None, optional): Number of seconds before timeout.
                If `None`, it will default to httpx.Client default 5 seconds.
                Defaults to 5.

        Returns:
            Response: Raw response from the JUDLIBRE API.
        """
        url = f"{self.judilibre_api_url.rstrip('/')}/{url.lstrip('/')}"

        params = self._clean_params(params)

        self._logger.info(f"REQUEST METHOD URL:            {method} {url}")
        self._logger.info(f"REQUEST PARAMETERS: {params}")

        response = self._client.request(
            method=method,
            url=url,
            params=params,
            timeout=timeout,
        )

        self._logger.info(f"RESPONSE STATUS : {response.status_code}")
        self._logger.info(f"RESPONSE HEADERS: {response.headers}")
        self._logger.debug(f"RESPONSE CONTENT: {response.content.decode('utf-8')}")

        response = catch_response(response=response)

        return response

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

    def decision(
        self,
        decision_id: str,
        *,
        timeout: int | None = 5,
    ) -> JudilibreDecision:
        """Retrieves a decision from **JUDILIBRE** based on its ID

        Args:
            decision_id (str): ID of the decision on **JUDILIBRE** ("5fca9d7b5f8d5e93418f86af" for example)
            timeout (int | None, optional): Number of seconds before timeout.
                If `None`, it will default to httpx.Client default 5 seconds.
                Defaults to 5.

        Raises:
            JudilibreDecisionNotFoundError: raised if the decision is not found on **JUDILIBRE**

        Returns:
            judilibre_decision (JudilibreDecision): a decision from **JUDILIBRE**
        """
        params = {
            "id": decision_id,
            "resolve_references": True,
        }
        try:
            response = self._query(
                method="GET",
                url="/decision",
                params=params,
                timeout=timeout,
            )
        except JudilibreResourceNotFoundError as exc:
            raise JudilibreDecisionNotFoundError(f"decision with ID {decision_id} not Found") from exc

        return JudilibreDecision(**response.json())

    def stats(
        self,
        *,
        keys: list[JudilibreStatsAggregationKeysEnum] | None = None,
        locations: list[LocationCAEnum | LocationTJEnum | LocationTCOMEnum] | None = None,
        jurisdictions: list[JurisdictionEnum] | None = None,
        date_start: datetime.date | None = None,
        date_end: datetime.date | None = None,
        date_type: JudilibreDateTypeEnum | None = JudilibreDateTypeEnum.creation,
        selection: bool | None = None,
        timeout: int | None = 5,
    ) -> JudilibreStats:
        """Returns aggregated statistics on the decisions available in **JUDILIBRE**

        Args:
            keys (list[JudilibreStatsAggregationKeysEnum] | None, optional): list of aggregation keys to group decision numbers by.
                Defaults to None.
            locations (list[LocationCAEnum  |  LocationTJEnum  |  LocationTCOMEnum] | None, optional): list of locations (courts) to return results from.
                If `None`, it will defaul to **JUDILIBRE** default settings.
                Defaults to None.
            jurisdictions (list[JurisdictionEnum] | None, optional): list of jurisdictions to return results from.
                If `None`, it will default to **JUDILIBRE** default settings.
                Defaults to None.
            date_start (datetime.date | None, optional): minimal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            date_end (datetime.date | None, optional): maximal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            date_type (str | None, optional): Type of date to use for the filters. Defaults to "creation".

            selection (bool | None, optional): Returns only results about decisions with a particular interest if true.
                If False, returns all the results
                Defaults to None.
            timeout (int | None, optional): Number of seconds before timeout.
                If `None`, it will default to httpx.Client default 5 seconds.
                Defaults to 5.

        Returns:
            JudilibreStats: A set of statistics correponding to the given aggregation keys and filters
        """
        params = {
            **({"keys": keys} if keys is not None else {}),
            **({"date_start": date_start} if date_start is not None else {}),
            **({"date_end": date_end} if date_end is not None else {}),
            **({"date_type": date_type} if date_type else {}),
            **({"jurisdiction": jurisdictions} if jurisdictions is not None else {}),
            **({"location": locations} if locations is not None else {}),
            **({"particularInterest": "true"} if selection else {}),
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
        locations: list[LocationCAEnum | LocationTJEnum | LocationTCOMEnum] | None = None,
        selection: bool | None = None,
        date_start: datetime.date | None = None,
        date_end: datetime.date | None = None,
        date_type: JudilibreDateTypeEnum | None = JudilibreDateTypeEnum.creation,
        timeout: int | None = 5,
        **kwargs,
    ) -> tuple[int, list[JudilibreDecision] | list[JudilibreShortDecision]]:
        """Returns a list of decisions based on a metadata query

        Args:
            batch_number (int, optional): Number of the batch to get.
                Defaults to 0.
            batch_size (int, optional): Size of the batch to get.
                Defaults to 10.
            jurisdictions (list[JurisdictionEnum] | None, optional): list of jurisdictions to return results from.
                If `None`, it will default to **JUDILIBRE** default settings.
                Defaults to None.
            locations (list[LocationCAEnum  |  LocationTJEnum  |  LocationTCOMEnum] | None, optional): list of locations (courts) to return results from.
                If `None`, it will defaul to **JUDILIBRE** default settings.
                Defaults to None.
            selection (bool | None, optional): Returns only results about decisions with a particular interest if true.
                If False, returns all the results
                Defaults to None.
            date_start (datetime.date | None, optional): minimal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            date_end (datetime.date | None, optional): maximal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            date_type (JudilibreDateTypeEnum | None, optional): Type of date to use for the filters.
                Defaults to `None`.
            timeout (int | None, optional): Number of seconds before timeout.
                If `None`, it will default to httpx.Client default 5 seconds.
                Defaults to 5.

        Returns:
            tuple[int, list[JudilibreDecision]]: a tuple containing the total number of decisions and the decisions corresponding to the current batch
        """
        params = {}

        params = {
            **({"particularInterest": "true"} if selection else {}),
            **({"location": locations} if locations else {}),
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
            timeout=timeout,
        )
        response_data = response.json()

        if params.get("abridged") is True:
            decisions = [JudilibreShortDecision(**d) for d in response_data["results"]]
        else:
            decisions = [JudilibreDecision(**d) for d in response_data["results"]]

        return (
            response_data["total"],
            decisions,
        )

    def search(
        self,
        query: str,
        page_size: int = 25,
        page_number: int = 0,
        *,
        operator: JudilibreOperatorEnum | None = None,
        jurisdictions: list[JurisdictionEnum] | None = None,
        locations: list[LocationCAEnum | LocationTJEnum | LocationTCOMEnum] | None = None,
        selection: bool | None = None,
        date_start: datetime.date | None = None,
        date_end: datetime.date | None = None,
        date_type: JudilibreDateTypeEnum | None = JudilibreDateTypeEnum.creation,
        timeout: int | None = 5,
        **kwargs,
    ) -> tuple[int, list[JudilibreSearchResult]]:
        """Returns search results based on a plain text query

        Args:
            query (str): a plain text query
            page_size (int, optional): number of results for the page.
                Defaults to 25.
            page_number (int, optional): number of the page.
                Defaults to 0.
            operator (JudilibreOperatorEnum | None, optional): operator to use for the search.
                If `None`, it will defaul to **JUDILIBRE** default settings.
                Defaults to None.            jurisdictions (list[JurisdictionEnum] | None, optional): list of jurisdictions to return results from.
                If `None`, it will default to **JUDILIBRE** default settings.
                Defaults to None.
            locations (list[LocationCAEnum  |  LocationTJEnum  |  LocationTCOMEnum] | None, optional): list of locations (courts) to return results from.
                If `None`, it will defaul to **JUDILIBRE** default settings.
                Defaults to None.
            selection (bool | None, optional): Returns only results about decisions with a particular interest if true.
                If False, returns all the results
                Defaults to None.
            date_start (datetime.date | None, optional): minimal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            date_end (datetime.date | None, optional): maximal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            timeout (int | None, optional): Number of seconds before timeout.
                If `None`, it will default to httpx.Client default 5 seconds.
                Defaults to 5.

        Returns:
            tuple[int, list[JudilibreSearchResult]]: a tuple containing the total number of search results and the list of results corresponding to the current page
        """
        params = {
            **({"particularInterest": "true"} if selection else {}),
            **({"location": locations} if locations else {}),
            **({"date_start": date_start} if date_start else {}),
            **({"date_end": date_end} if date_end else {}),
            **({"operator": operator} if operator else {}),
            **({"jurisdiction": jurisdictions} if jurisdictions else {}),
            **({"date_type": date_type} if date_type else {}),
            **kwargs,
            "query": query,
            "page_size": page_size,
            "page": page_number,
            "resolve_references": True,
        }

        response = self._query(
            method="GET",
            url="/search",
            params=params,
            timeout=timeout,
        )
        response_data = response.json()

        return (
            response_data["total"],
            [JudilibreSearchResult(**r) for r in response_data["results"]],
        )

    def scan(
        self,
        batch_size: int = 100,
        *,
        jurisdictions: list[JurisdictionEnum] | None = None,
        locations: list[LocationCAEnum | LocationTJEnum | LocationTCOMEnum] | None = None,
        selection: bool | None = None,
        date_start: datetime.date | None = None,
        date_end: datetime.date | None = None,
        date_type: JudilibreDateTypeEnum | None = JudilibreDateTypeEnum.creation,
        search_after: str | None = None,
        timeout: int | None = 5,
        **kwargs,
    ) -> tuple[int, list[JudilibreDecision] | list[JudilibreShortDecision], str | None]:
        """Returns a list of decisions based on a metadata query

        Args:
            search_after (str, optional): ID of the decision that will start the batch.
                Defaults to 0.
            batch_size (int, optional): Size of the batch to get.
                Defaults to 10.
            jurisdictions (list[JurisdictionEnum] | None, optional): list of jurisdictions to return results from.
                If `None`, it will default to **JUDILIBRE** default settings.
                Defaults to None.
            locations (list[LocationCAEnum  |  LocationTJEnum  |  LocationTCOMEnum] | None, optional): list of locations (courts) to return results from.
                If `None`, it will defaul to **JUDILIBRE** default settings.
                Defaults to None.
            selection (bool | None, optional): Returns only results about decisions with a particular interest if true.
                If False, returns all the results
                Defaults to None.
            date_start (datetime.date | None, optional): minimal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            date_end (datetime.date | None, optional): maximal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            date_type (JudilibreDateTypeEnum | None, optional): Type of date to use for the filters.
                If `None`, it will default to **JUDILIBRE** default settings.
                Defaults to JudilibreDateTypeEnum.creation.
            timeout (int | None, optional): Number of seconds before timeout.
                If `None`, it will default to httpx.Client default 5 seconds.
                Defaults to 5.

        Returns:
            tuple[int, list[JudilibreDecision], str | None]: a tuple containing:
                - the total number of decisions
                - the decisions corresponding to the current batch
                - the id to provide for the next batch
        """
        params = {
            **({"particularInterest": "true"} if selection else {}),
            **({"location": locations} if locations else {}),
            **({"jurisdiction": jurisdictions} if jurisdictions else {}),
            **({"date_start": date_start} if date_start else {}),
            **({"date_end": date_end} if date_end else {}),
            **({"date_type": date_type} if date_type else {}),
            **({"searchAfter": search_after} if search_after else {}),
            "resolve_references": True,
            "batch_size": batch_size,
            **kwargs,
        }

        response = self._query(
            method="GET",
            url="/scan",
            params=params,
            timeout=timeout,
        )

        response_data = response.json()

        total_decisions = response_data["total"]
        if params.get("abridged") is True:
            decisions = [JudilibreShortDecision(**d) for d in response_data["results"]]
        else:
            decisions = [JudilibreDecision(**d) for d in response_data["results"]]
        search_after = parse_qs(response_data["next_batch"]).get("searchAfter", [None])[0]

        return (
            total_decisions,
            decisions,
            search_after,
        )

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
        timeout: int | None = 5,
    ) -> dict[str, str]:
        """Returns a dictionary of key-value pairs corresponding to a taxon.
        If a `taxon_key` or a `taxon_value` is given, it will only return the dictionary for this particular key or value.

        Args:
            taxon_id (JudilibreTaxonEnum): name of the taxon to get information on
            context (JurisdictionEnum): jurisdisction type (taxons can be different for different types of jurisdictions)
            taxon_key (str | None, optional): a key of a taxon we want the value to.
                Defaults to None.
            taxon_value (str | None, optional): a value of a taxon we want the value to.
                Defaults to None.
            timeout (int | None, optional): Number of seconds before timeout.
                If `None`, it will default to httpx.Client default 5 seconds.
                Defaults to 5.

        Raises:
            ValueError: if both `taxon_key` and `taxon_value` are given

        Returns:
            dict[str, str]: a dictionary of key-value pairs corresponding to a taxon
        """
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
            timeout=timeout,
        )

        response_data = response.json()

        taxons: dict[str, str] = {}

        if taxon_key is not None:
            taxons[taxon_key] = response_data["result"]["value"]
        elif taxon_value is not None:
            taxons[response_data["result"]["key"]] = taxon_value
        else:
            taxons = response_data["result"]

        return taxons

    def transactional_history(
        self,
        date_start: datetime.date,
        *,
        page_size: int = 25,
        from_id: str | None = None,
        timeout: int | None = 5,
    ) -> tuple[int, list[JudilibreTransaction], str | None]:
        """Returns the list of transactions after a given date

        Args:
            date_start (datetime.date): mininmal date for the transactions
            page_size (int, optional): Number of results to return at once.
                Defaults to 25.
            from_id (str | None, optional): ID of the previous query to paginate results.
                Defaults to None.
            timeout (int | None, optional): Number of seconds before timeout.
                If `None`, it will default to httpx.Client default 5 seconds.
                Defaults to 5.

        Returns:
            tuple[int, list[JudilibreTransaction], str]: (
                - total number of transactions after `start_date`
                - list of transactions
                - ID of the query to paginate results
            )
        """
        params = {
            "date": date_start,
            "page_size": page_size,
            **({"from_id": from_id} if from_id else {}),
        }

        response = self._query(
            method="GET",
            url="transactionalhistory",
            params=params,
            timeout=timeout,
        )

        response_data = response.json()
        total_transactions = response_data["total"]
        next_from_id: str = parse_qs(response_data["next_page"]).get("from_id", [None])[0]
        transactions = [JudilibreTransaction(**t) for t in response_data["transactions"]]

        return (
            total_transactions,
            transactions,
            next_from_id,
        )

    def paginate_search(
        self,
        query: str,
        max_results: int | None = None,
        *,
        jurisdictions: list[JurisdictionEnum] | None = None,
        locations: list[LocationCAEnum | LocationTJEnum | LocationTCOMEnum] | None = None,
        selection: bool | None = None,
        operator: JudilibreOperatorEnum | None = None,
        date_start: datetime.date | None = None,
        date_end: datetime.date | None = None,
        date_type: JudilibreDateTypeEnum | None = JudilibreDateTypeEnum.creation,
        timeout: int | None = 5,
        **kwargs,
    ) -> list[JudilibreSearchResult]:
        """Paginates through all the results from a plain text query

        Args:
            query (str): plain text string query
            max_results (int | None, optional):  maximal number of results that should be returned.
                If `None` all results are returned.
                Defaults to None.
            jurisdictions (list[JurisdictionEnum] | None, optional): list of jurisdictions to return results from.
                If `None`, it will default to **JUDILIBRE** default settings.
                Defaults to None.
            locations (list[LocationCAEnum  |  LocationTJEnum  |  LocationTCOMEnum] | None, optional): list of locations (courts) to return results from.
                If `None`, it will defaul to **JUDILIBRE** default settings.
                Defaults to None.
            selection (bool | None, optional): Returns only results about decisions with a particular interest if true.
                If False, returns all the results
                Defaults to None.
            operator (JudilibreOperatorEnum | None, optional): operator to use for the search.
                If `None`, it will defaul to **JUDILIBRE** default settings.
                Defaults to None.
            date_start (datetime.date | None, optional): minimal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            date_end (datetime.date | None, optional): maximal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            timeout (int | None, optional): Number of seconds before timeout.
                If `None`, it will default to httpx.Client default 5 seconds.
                Defaults to 5.

        Returns:
            list[JudilibreSearchResult]: list of search results corresponding to the query
        """
        page_size = 25
        page_number = 0
        next_page = True

        params = {
            **({"particularInterest": "true"} if selection else {}),
            **({"location": locations} if locations else {}),
            **({"date_start": date_start} if date_start else {}),
            **({"date_end": date_end} if date_end else {}),
            **({"operator": operator} if operator else {}),
            **({"jurisdiction": jurisdictions} if jurisdictions else {}),
            **({"date_type": date_type} if date_type else {}),
            **kwargs,
            "query": query,
            "page_size": page_size,
            "page": page_number,
            "resolve_references": True,
        }

        results = []
        n_results = 0

        while next_page:
            params["page"] = page_number

            response = self._query(
                method="GET",
                url="/search",
                params=params,
                timeout=timeout,
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

    def paginate_export(
        self,
        max_results: int | None = None,
        *,
        jurisdictions: list[JurisdictionEnum] | None = None,
        locations: list[LocationCAEnum | LocationTJEnum | LocationTCOMEnum] | None = None,
        selection: bool | None = None,
        date_start: datetime.date | None = None,
        date_end: datetime.date | None = None,
        date_type: JudilibreDateTypeEnum | None = JudilibreDateTypeEnum.creation,
        timeout: int | None = 5,
        **kwargs,
    ) -> list[JudilibreDecision] | list[JudilibreShortDecision]:
        """Paginates through the results of a metadata query

        Args:
            max_results (int | None, optional):  maximal number of results that should be returned.
                If `None` all results are returned.
                Defaults to None.
            jurisdictions (list[JurisdictionEnum] | None, optional): list of jurisdictions to return results from.
                If `None`, it will default to **JUDILIBRE** default settings.
                Defaults to None.
            locations (list[LocationCAEnum  |  LocationTJEnum  |  LocationTCOMEnum] | None, optional): list of locations (courts) to return results from.
                If `None`, it will default to **JUDILIBRE** default settings.
                Defaults to None.
            selection (bool | None, optional): Returns only results about decisions with a particular interest if true.
                If False, returns all the results
                Defaults to None.
            date_start (datetime.date | None, optional): minimal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            date_end (datetime.date | None, optional): maximal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            date_type (JudilibreDateTypeEnum | None, optional): type of date to use for the date filters.
                If `None`, it will default to **JUDILIBRE** default settings.
                Defaults to JudilibreDateTypeEnum.creation.
            timeout (int | None, optional): Number of seconds before timeout.
                If `None`, it will default to httpx.Client default 5 seconds.
                Defaults to 5.

        Returns:
            list[JudilibreDecision]: list of decisions corresponding to the query
        """
        batch_size = 100
        batch_number = 0
        next_batch = True

        params = {
            **({"particularInterest": "true"} if selection else {}),
            **({"location": locations} if locations else {}),
            **({"jurisdiction": jurisdictions} if jurisdictions else {}),
            **({"date_start": date_start} if date_start else {}),
            **({"date_end": date_end} if date_end else {}),
            **({"date_type": date_type} if date_type else {}),
            "resolve_references": True,
            "batch": batch_number,
            "batch_size": batch_size,
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
                timeout=timeout,
            )

            response_data = response.json()
            if params.get("abridged") is True:
                new_decisions = [JudilibreShortDecision(**r) for r in response_data["results"]]
            else:
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

    def paginate_scan(
        self,
        batch_size: int = 100,
        *,
        jurisdictions: list[JurisdictionEnum] | None = None,
        locations: list[LocationCAEnum | LocationTJEnum | LocationTCOMEnum] | None = None,
        selection: bool | None = None,
        date_start: datetime.date | None = None,
        date_end: datetime.date | None = None,
        date_type: JudilibreDateTypeEnum | None = JudilibreDateTypeEnum.creation,
        max_results: int | None = None,
        verbose: bool = False,
        timeout: int | None = 5,
        **kwargs,
    ) -> list[JudilibreDecision] | list[JudilibreShortDecision]:
        """Paginates through the results of a metadata query

        Args:
            max_results (int | None, optional):  maximal number of results that should be returned.
                If `None` all results are returned.
                Defaults to None.
            jurisdictions (list[JurisdictionEnum] | None, optional): list of jurisdictions to return results from.
                If `None`, it will default to **JUDILIBRE** default settings.
                Defaults to None.
            locations (list[LocationCAEnum  |  LocationTJEnum  |  LocationTCOMEnum] | None, optional): list of locations (courts) to return results from.
                If `None`, it will default to **JUDILIBRE** default settings.
                Defaults to None.
            selection (bool | None, optional): Returns only results about decisions with a particular interest if true.
                If False, returns all the results
                Defaults to None.
            date_start (datetime.date | None, optional): minimal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            date_end (datetime.date | None, optional): maximal date to return results from.
                If `None` returns all the results.
                Defaults to None.
            date_type (JudilibreDateTypeEnum | None, optional): type of date to use for the date filters.
                If `None`, it will default to **JUDILIBRE** default settings.
                Defaults to JudilibreDateTypeEnum.creation.
            timeout (int | None, optional): Number of seconds before timeout.
                If `None`, it will default to httpx.Client default 5 seconds.
                Defaults to 5.

        Returns:
            list[JudilibreDecision]: list of decisions corresponding to the query
        """
        decisions: list[JudilibreDecision | JudilibreShortDecision] = []
        n_decisions = 0

        progression_bar = None

        stats = self.stats(
            jurisdictions=jurisdictions,
            locations=locations,
            date_start=date_start,
            date_end=date_end,
            date_type=date_type,
            timeout=timeout,
        )

        if verbose:
            if (max_results is not None) and (stats.results.total_decisions is not None):
                progression_bar = tqdm(
                    total=min(
                        max_results,
                        stats.results.total_decisions,
                    )
                )
            else:
                progression_bar = tqdm(total=stats.results.total_decisions)

        total, decisions_tmp, search_after = self.scan(
            jurisdictions=jurisdictions,
            locations=locations,
            selection=selection,
            date_start=date_start,
            date_end=date_end,
            date_type=date_type,
            batch_size=batch_size,
            timeout=timeout,
            **kwargs,
        )

        n_decisions += len(decisions_tmp)

        if verbose and progression_bar:
            progression_bar.update(len(decisions_tmp))

        decisions.extend(decisions_tmp)

        def end_condition(
            search_after,
            max_results,
            n_decisions,
        ):
            if search_after is None:
                return True
            if max_results is None:
                return False
            if n_decisions >= max_results:
                return True

        while not end_condition(
            search_after=search_after,
            max_results=max_results,
            n_decisions=n_decisions,
        ):
            total, decisions_tmp, search_after = self.scan(
                jurisdictions=jurisdictions,
                locations=locations,
                selection=selection,
                date_start=date_start,
                date_end=date_end,
                date_type=date_type,
                search_after=search_after,
                batch_size=batch_size,
                timeout=timeout,
                **kwargs,
            )

            if verbose and progression_bar:
                progression_bar.update(len(decisions_tmp))

            n_decisions += len(decisions_tmp)
            decisions.extend(decisions_tmp)
        if max_results is not None:
            return decisions[:max_results]
        return decisions

    def paginate_transactional_history(
        self,
        date_start: datetime.datetime,
        *,
        max_results: int | None = None,
        timeout: int | None = 5,
    ) -> list[JudilibreTransaction]:
        """Paginates through the transactional history results

            Args:
                date_start (datetime.datetime): minimal date to return results from.
                max_results (int | None, optional):  maximal number of results that should be returned.
                If `None` all results are returned.

        Defaults to None.

            Returns:
                list[JudilibreTransaction]: list of transaction corresponding to the query
        """
        page_size = 500

        _, transactions, from_id = self.transactional_history(
            date_start=date_start,
            page_size=page_size,
            timeout=timeout,
        )
        n_transactions = len(transactions)

        def end_condition(
            from_id,
            max_results,
            n_transactions,
        ):
            if from_id is None:
                return True
            if max_results is None:
                return False
            if n_transactions >= max_results:
                return True

        while not end_condition(
            from_id=from_id,
            max_results=max_results,
            n_transactions=n_transactions,
        ):
            _, tmp_transactions, from_id = self.transactional_history(
                date_start=date_start,
                from_id=from_id,
                timeout=timeout,
            )
            n_transactions += len(tmp_transactions)
            transactions += tmp_transactions

        transactions = transactions[:max_results]

        return transactions
