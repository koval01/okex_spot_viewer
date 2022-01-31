import json
import os
from time import time

from requests import get as http_get


class OkxApi:
    def __init__(self, index: int = 0) -> None:
        self.host = "www.okx.com"
        self.path = "priapi/v5/algo/trade/info"
        self.params = {
            "t": round(time()),
            "algoId": os.getenv("ALGO_ID").split()[index]
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

    @staticmethod
    def short_id(id_: str) -> str:
        return f"{'*' * (len(id_) - 6)}{id_[-6:]}"

    def get(self) -> dict:
        return self.request().json()
