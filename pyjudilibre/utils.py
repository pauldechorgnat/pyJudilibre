import datetime
import math

import requests
from tqdm import tqdm

from .decorators import catch_wrong_url_error
from .exceptions import JudilibreValueError, JudilibreWrongCredentialsError

AVAILABLE_ACTIONS = set(["raise", "warn", "ignore"])


# def check_value(
#     value: str,
#     value_name: str = "",
#     message: Union[str, None] = None,
#     allowed_values: Union[list[str], dict[str, str], set[str]] = [],
#     action_on_check: str = "raise",
# ) -> bool:
#     """Function that check if a value is in a set of allowed values and acts on it.

#     Args:
#         value (str): value of the parameter to check
#         value_name (str, optional): name of the parameter to check.
#             Defaults to "".
#         allowed_values (list[str], optional): list or set of allowed values.
#             Defaults to [].
#         action_on_check (str, optional): action to take if the check is not valid.
#             Must be one of "raise", "warn" or "ignore"
#             Defaults to "raise".

#     Raises:
#         ValueError: raised if the value of action_on_check is not valid.
#         JudilibreValueError: raised if the value of the parameter is not valid.

#     Returns:
#         bool: True if the parameter is a valid value. False otherwise.
#     """
#     if action_on_check not in AVAILABLE_ACTIONS:
#         raise ValueError(
#             "'action_on_check' should be one of ['raise', 'warn', 'ignore']. "
#             f"Received '{action_on_check}'"
#         )
#     if message is None:
#         message = f"'{value}' is not a valid value for parameter '{value_name}'"
#     else:
#         message = message.format(
#             value=value,
#             value_name=value_name,
#         )

#     if value not in allowed_values:
#         if action_on_check == "raise":
#             raise JudilibreValueError(message)
#         elif action_on_check == "warn":
#             warnings.warn(message, category=JudilibreValueWarning)
#             return False
#         elif action_on_check == "ignore":
#             return False

#     return True


def check_authentication_error(response: requests.Response) -> None:
    """Checks if a CredentialError is raised.

    Args:
        response (requests.Response): response

    Raises:
        JudilibreWrongCredentialsError: raised if status code is 400.
    """
    if response.status_code == 400:
        message = response.headers.get("WWW-Authenticate", "")
        if message == (
            'Bearer realm="DefaultRealm",error="invalid_request"'
            ',error_description="Unable to find token in the message"'
        ):
            raise JudilibreWrongCredentialsError("Credentials are not valid.")


@catch_wrong_url_error
def paginate_results(
    url: str,
    parameters: dict = {},
    headers: dict = {},
    batch_size: int = 10,
    max_results: int = 10_000,
    verbose: bool = False,
    batch_type: str = "batch",
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
        raise JudilibreValueError(
            f"'{batch_type}' parameter cannot be more than 1,000."
        )
    elif batch_size < 1:
        raise JudilibreValueError(f"'{batch_type}' parameter cannot be less than 1.")

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

    parameters[f"{batch_type}_size"] = batch_size

    for index_batch in batch_numbers:
        parameters[batch_type] = index_batch

        response = requests.get(url=url, headers=headers, params=parameters)

        check_authentication_error(response=response)

        data = response.json()

        if "results" in data:
            if index_batch != n_batches - 1:
                decisions.extend(response.json()["results"])
                n_decisions += batch_size
            else:
                decisions.extend(response.json()["results"][:remaining_results])
                n_decisions += remaining_results

        else:
            break

        if verbose:
            batch_numbers.set_description(
                f"{str(n_decisions).zfill(n_zeros)}/"
                f"{str(max_results).zfill(n_zeros)} decisions"
            )

        if response.json()[f"next_{batch_type}"] is None:
            break

    return decisions


def check_date(
    input_date: str,
) -> bool:
    try:
        datetime.date.fromisoformat(input_date)
        return True
    except ValueError as exc:
        raise JudilibreValueError(f"'{input_date}' is not a valid date format") from exc


def check_value(
    value,
    value_name: str,
    authozied_values: list = [],
) -> bool:
    if value in authozied_values:
        return True
    raise JudilibreValueError(
        f"`{value}` is not a valid value for parameter `{value_name}`"
    )
