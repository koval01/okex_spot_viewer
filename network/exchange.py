import json
import os
from time import time

from requests import get as http_get


class ExchangeData:
    def __init__(self, exchange: str = "TONCOIN_USDT") -> None:
        self.host = "www.okx.com"
        self.path = "priapi/v5/market/mult-tickers"
        self.params = {
            "t": round(time()),
            "instIds": exchange
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
