import json
import os

from flask import jsonify

from models.grid import Model as ModelGrid
from models.trades import Model as ModelTrades
from network.currency import CurrencyGet
from network.grid import OkxApi
from network.trades import TradesGrid


class GridJson:
    def __init__(self) -> None:
        self.hints = json.loads(open(
            os.path.dirname(os.path.abspath(__file__)) + '/../other/hints.json', "r"
        ).read())["hint"]
        self.uah_price = CurrencyGet().get()
        self.trades_data = TradesGrid().get()
        self.grid_data = OkxApi().get()

    @staticmethod
    def data_round(value: str) -> float:
        return round(float(value), 3)

    def build_trades_data(self) -> list:
        return [{
            "trade_time": int(el.tradeTime),
            "profit": self.data_round(el.totalPnl),
            "profit_uah": self.data_round(el.totalPnl) * self.uah_price
        } for el in ModelTrades(**self.trades_data).data]

    def build_grid_data(self) -> dict:
        data = ModelGrid(**self.grid_data).data[0]
        uah_price = self.uah_price
        return {
            "algo_id": OkxApi().short_id(data.algoId),
            "annualized_rate": round(float(data.annualizedRate), 3),
            "annualized_rate_uah": round(float(data.annualizedRate) * uah_price, 3),
            "profit": round(float(data.gridProfit), 3),
            "profit_uah": round(float(data.gridProfit) * uah_price, 3),
            "float_profit": round(float(data.floatProfit), 3),
            "float_profit_uah": round(float(data.floatProfit) * uah_price, 3),
            "total_price": round(float(data.totalPnl), 3),
            "total_price_uah": round(float(data.totalPnl) * uah_price, 3),
            "run-price": round(float(data.runPx), 3),
            "run-price_uah": round(float(data.runPx) * uah_price, 3),
            "trades_num": int(data.tradeNum),
            "arbitrages_num": int(data.arbitrageNum),
            "created_at_utc": int(data.cTime),
            "instance_id": str(data.instId),
            "instance_type": str(data.instType),
            "order_type": str(data.ordType),
        }

    def get(self) -> jsonify:
        try:
            data_trades = self.build_trades_data()
            data_grid = self.build_grid_data()
            return jsonify({
                "success": len(self.grid_data["data"]) > 0 and len(data_trades) > 0,
                "trades": data_trades,
                "data": data_grid,
                "hint": self.hints
            })
        except Exception as e:
            return jsonify({"success": False, "exception": str(e)})
