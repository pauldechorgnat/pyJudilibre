import functools

import requests

from .exceptions import JudilibreWrongURLError


def catch_wrong_url_error(function: callable):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            results = function(*args, **kwargs)
            return results
        except requests.exceptions.ConnectionError as exc:
            raise JudilibreWrongURLError("URL is not reachable.") from exc

    return wrapper
