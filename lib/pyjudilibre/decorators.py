import functools
from typing import Callable

import httpx
from pyjudilibre.exceptions import JudilibreWrongURLError


def catch_wrong_url_error(function: Callable):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            results = function(*args, **kwargs)
            return results
        except httpx.ConnectError as exc:
            raise JudilibreWrongURLError("URL is not reachable.") from exc

    return wrapper
