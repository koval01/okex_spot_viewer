import json
import os
from time import time

from requests import get as http_get


class Profit:
    def __init__(self) -> None:
        self.host = "www.okx.com"
        self.path = "priapi/v5/algo/grid/trade-list"
        self.params = {
            "t": round(time()),
            "algoId": os.getenv("ALGO_ID")
        }
        self.headers = {
            "Authorization": os.getenv("AUTH_KEY")
        }

    def request(self) -> http_get:
        return http_get(
            url=f"https://{self.host}/{self.path}",
            params=self.params, headers=self.headers
        )

    def __str__(self) -> str:
        return json.dumps(obj=self.request().json(), indent=5)

    def get(self) -> dict:
        return self.request().json()
