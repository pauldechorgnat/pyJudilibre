import functools
from typing import Callable

import httpx

from pyjudilibre.exceptions import JudilibreWrongURLError


def catch_wrong_url_error(function: Callable):
    """Utility wrapper to catch errors in URL

    Args:
        function (Callable): function to call

    Raises:
        JudilibreWrongURLError: raised if URL is wrong

    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        """Wrapped function"""
        try:
            results = function(*args, **kwargs)
            return results
        except httpx.ConnectError as exc:
            raise JudilibreWrongURLError("URL is not reachable.") from exc

    return wrapper
