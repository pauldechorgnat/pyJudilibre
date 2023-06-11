import datetime
import math
import warnings
from typing import Union

import requests
from tqdm import tqdm

from .decorators import catch_wrong_url_error
from .exceptions import (
    JudilibreValueError,
    JudilibreValueWarning,
    JudilibreWrongCredentialsError,
)

AVAILABLE_ACTIONS = set(["raise", "warn", "ignore"])


def check_value(
    value: str,
    value_name: str = "",
    message: Union[str, None] = None,
    allowed_values: Union[list[str], dict[str, str], set[str]] = [],
    action_on_check: str = "raise",
) -> bool:
    """Function that check if a value is in a set of allowed values and acts on it.

    Args:
        value (str): value of the parameter to check
        value_name (str, optional): name of the parameter to check.
            Defaults to "".
        allowed_values (list[str], optional): list or set of allowed values.
            Defaults to [].
        action_on_check (str, optional): action to take if the check is not valid.
            Must be one of "raise", "warn" or "ignore"
            Defaults to "raise".

    Raises:
        ValueError: raised if the value of action_on_check is not valid.
        JudilibreValueError: raised if the value of the parameter is not valid.

    Returns:
        bool: True if the parameter is a valid value. False otherwise.
    """
    if action_on_check not in AVAILABLE_ACTIONS:
        raise ValueError(
            "'action_on_check' should be one of ['raise', 'warn', 'ignore']. "
            f"Received '{action_on_check}'"
        )
    if message is None:
        message = f"'{value}' is not a valid value for parameter '{value_name}'"
    else:
        message = message.format(value=value, value_name=value_name)

    if value not in allowed_values:
        if action_on_check == "raise":
            raise JudilibreValueError(message)
        elif action_on_check == "warn":
            warnings.warn(message, category=JudilibreValueWarning)
        elif action_on_check == "ignore":
            return False

    return True


def check_authentication_error(status_code: int) -> None:
    """Checks if the status code is 400 which means a CredentialError.

    Args:
        status_code (int): status code of a requests

    Raises:
        JudilibreWrongCredentialsError: raised if status code is 400.
    """
    if status_code == 400:
        raise JudilibreWrongCredentialsError("Credentials are not valid.")


@catch_wrong_url_error
def paginate_results(
    url: str,
    parameters: dict = {},
    headers: dict = {},
    batch_size: int = 10,
    max_results: int = 10_000,
    verbose: bool = False,
) -> list[dict]:
    """_summary_

    Args:
        url (str): url of the request
        parameters (dict, optional): parameters of the request.
            Defaults to {}.
        headers (dict, optional): headers of the request.
            Defaults to {}.
        batch_size (int, optional): size of the batches.
            Defaults to 10.
        max_results (int, optional): maximum number of results to return.
            Defaults to 10_000.
        verbose (bool, optional): if True shows a progress bar.
            Defaults to False.

    Raises:
        JudilibreValueError: raised if 'batch_size' is more than 1,000.
        JudilibreValueError: raised if 'batch_size' is less than 1.
        JudilibreValueError: raised if 'max_results' is more than 10, 000.
        JudilibreValueError: raised if 'max_results' is less than 1

    Returns:
        list[dict]: a list of decisions as a dictionaries
    """
    if batch_size > 1_000:
        raise JudilibreValueError("'batch_size' parameter cannot be more than 1,000.")
    elif batch_size < 1:
        raise JudilibreValueError("'batch_size' parameter cannot be less than 1.")

    if max_results > 10_000:
        raise JudilibreValueError(
            "Judilibre cannot return more than 10,000 results for a given query."
        )
    elif max_results < 1:
        raise JudilibreValueError("'max_results' cannot be less than 1.")

    if max_results < batch_size:
        batch_size = max_results

    n_batches = (max_results // batch_size) + 1
    remaining_results = max_results % batch_size

    decisions = []
    n_decisions = 0

    if verbose:
        batch_numbers = tqdm(range(n_batches))
        n_zeros = int(math.log10(max_results) + 1)
        batch_numbers.set_description(
            f"{str(n_decisions).zfill(n_zeros)}/"
            f"{str(max_results).zfill(n_zeros)} decisions"
        )
    else:
        batch_numbers = range(n_batches)

    parameters["batch_size"] = batch_size

    for index_batch in batch_numbers:
        parameters["batch"] = index_batch

        response = requests.get(url=url, headers=headers, params=parameters)

        check_authentication_error(status_code=response.status_code)

        if index_batch != n_batches - 1:
            decisions.extend(response.json()["results"])
            n_decisions += batch_size
        else:
            decisions.extend(response.json()["results"][:remaining_results])
            n_decisions += remaining_results

        if verbose:
            batch_numbers.set_description(
                f"{str(n_decisions).zfill(n_zeros)}/"
                f"{str(max_results).zfill(n_zeros)} decisions"
            )

        if response.json()["next_batch"] is None:
            break

    return decisions


def check_date(input_date: str, action_on_check: str = "raise") -> str:
    if action_on_check not in AVAILABLE_ACTIONS:
        raise ValueError(
            "'action_on_check' should be one of ['raise', 'warn', 'ignore']. "
            f"Received '{action_on_check}'"
        )
    try:
        datetime.date.fromisoformat(input_date)
        return True
    except ValueError as exc:
        if action_on_check == "raise":
            raise JudilibreValueError(
                f"'{input_date}' is not a valid date format"
            ) from exc
        elif action_on_check == "warn":
            warnings.warn(
                f"'{input_date}' is not a valid date format",
                category=JudilibreValueWarning,
            )
        else:
            return False
