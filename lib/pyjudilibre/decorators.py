import functools
from typing import Callable


from pyjudilibre.exceptions import JudilibreWrongURLError
import httpx


def catch_wrong_url_error(function: Callable):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            results = function(*args, **kwargs)
            return results
        except httpx.ConnectError as exc:
            raise JudilibreWrongURLError("URL is not reachable.") from exc

    return wrapper
