from network.currency import CurrencyGet


class Currency:
    def __init__(self, data_json: dict, currency_iso: str = "UAH") -> None:
        self.variables = [
            "annualized_rate", "investment",
            "profit", "float_profit",
            "total_price", "run-price"
        ]
        self.data_json = data_json
        self.currency_iso = currency_iso

    def usd_uah(self) -> float:
        return CurrencyGet().get()

    def get(self) -> list:
        pass
