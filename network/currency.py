import logging

import requests_cache


class CurrencyGet:
    def __init__(self, mode: str = "USD") -> None:
        self.session = requests_cache.CachedSession(
            name="CurrencyGet", backend="memory",
            expire_after=300,
            cache_control=False,
        )
        self.host = "bank.gov.ua"
        self.path = "NBUStatService/v1/statdirectory/exchange"
        self.mode = mode
        self.params = {"json": ""}

    def get(self) -> float:
        try:
            resp = self.session.get(
                url=f"https://{self.host}/{self.path}",
                params=self.params
            )
            logging.info("%s status code: %d" % (CurrencyGet.__name__, resp.status_code))
            return [el["rate"] for el in resp.json() if el["cc"] == self.mode][0]
        except Exception as e:
            logging.error("%s: %s" % (CurrencyGet.__name__, e))
            return 0.0
