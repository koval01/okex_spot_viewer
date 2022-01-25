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

    def request(self) -> dict or None:
        try:
            resp = self.session.get(
                url=f"https://{self.host}/{self.path}",
                params=self.params
            )
            logging.info("%s status code: %d" % (CurrencyGet.__name__, resp.status_code))
            return resp.json()
        except Exception as e:
            logging.error("%s.%s: %s" % (CurrencyGet.__name__, self.request.__name__, e))

    def get_currency(self, currency: str = "USD") -> float:
        try:
            return [el["rate"] for el in self.request() if el["cc"] == currency][0]
        except Exception as e:
            logging.error("%s.%s: %s" % (CurrencyGet.__name__, self.get_currency.__name__, e))
            return 0.0

    def other_currency(self, currency: str = "EUR") -> float:
        return self.get_currency() / self.get_currency(currency)

    def get(self) -> float:
        if self.mode == "USD":
            return self.get_currency()
        return self.other_currency(self.mode)
