import requests

from .exceptions import JudilibreWrongCredentials, JudilibreWrongURLError


class JudilibreClient:
    """Class that implements a Python Client for the Judilibre API"""

    def __init__(self, api_url: str, api_key_id: str):
        self.api_url = api_url
        self.api_key_id = api_key_id

        self.api_headers = {"KeyId": api_key_id}

    def search(self):
        pass

    def export(self):
        pass

    def get(self):
        pass

    def healthcheck(self):
        try:
            response = requests.get(
                url=f"{self.api_url}/healthcheck", headers=self.api_headers
            )

        except requests.exceptions.ConnectionError as exc:
            raise JudilibreWrongURLError(
                f"URL `{self.api_url}` is not reachable."
            ) from exc

        if response.status_code != 200:
            raise JudilibreWrongCredentials("Credentials are not valid.")

        if response.json()["status"]:
            return True

        return False
