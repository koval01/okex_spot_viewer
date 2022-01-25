import json
import os

from models.exchange import Model as ExchangeModel
from models.grid import Model as ModelGrid
from models.trades import Model as ModelTrades
from network.currency import CurrencyGet
from network.exchange import ExchangeData
from network.grid import OkxApi
from network.trades import TradesGrid


class GridJson:
    def __init__(self) -> None:
        self.hints = json.loads(open(
            os.path.dirname(os.path.abspath(__file__)) + '/../other/hints.json', "r"
        ).read())["hint"]
        self.currency = {
            "uah": CurrencyGet().get(),
            "rub": CurrencyGet("RUB").get(),
            "eur": CurrencyGet("EUR").get(),
            "pln": CurrencyGet("PLN").get()
        }
        self.trades_data = TradesGrid().get()
        self.grid_data = OkxApi().get()

    @staticmethod
    def data_round(value: str) -> float:
        return round(float(value), 3)

    def build_trades_data(self) -> list:
        return [{
            "trade_time": int(el.tradeTime),
            "profit": self.data_round(el.totalPnl),
        } for el in ModelTrades(**self.trades_data).data]

    def build_grid_data(self) -> dict:
        data = ModelGrid(**self.grid_data).data[0]
        currency = ExchangeModel(**ExchangeData(data.instId).get()).data[0]
        return {
            "algo_id": OkxApi().short_id(data.algoId),
            "annualized_rate": round(float(data.annualizedRate), 3),
            "profit": round(float(data.gridProfit), 3),
            "current_price": round(float(currency.last), 3),
            "float_profit": round(float(data.floatProfit), 3),
            "total_price": round(float(data.totalPnl), 3),
            "run-price": round(float(data.runPx), 3),
            "trades_num": int(data.tradeNum),
            "arbitrages_num": int(data.arbitrageNum),
            "created_at_utc": int(data.cTime),
            "was_launched": int(data.cTime),
            "instance_id": str(data.instId),
            "instance_type": str(data.instType),
            "order_type": str(data.ordType),
        }

    def get(self) -> dict:
        try:
            data_trades = self.build_trades_data()
            data_grid = self.build_grid_data()
            return {
                "success": len(self.grid_data["data"]) > 0 and len(data_trades) > 0,
                "trades": data_trades,
                "data": data_grid,
                "hint": self.hints,
                "currency": self.currency,
            }
        except Exception as e:
            return {"success": False, "exception": str(e)}
