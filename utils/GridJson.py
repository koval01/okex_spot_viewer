from flask import jsonify

from models.grid import Model as ModelGrid
from models.trades import Model as ModelTrades
from network.currency import CurrencyGet
from network.grid import OkxApi
from network.trades import TradesGrid


class GridJson:
    @staticmethod
    def getData() -> jsonify:
        try:
            uah_price = CurrencyGet().get()
            loads = OkxApi().get()
            loads_trades = TradesGrid().get()
            data = ModelGrid(**loads).data[0]
            data_trades = [{
                "trade_id": int(el.groupId),
                "trade_time": int(el.tradeTime),
                "profit": round(float(el.totalPnl), 3),
                "profit_uah": round(float(el.totalPnl) * uah_price, 3)
            } for el in ModelTrades(**loads_trades).data]
            return jsonify({
                "success": len(loads["data"]) > 0 and len(data_trades) > 0,
                "trades": data_trades,
                "data": {
                    "algo_id": OkxApi().short_id(data.algoId),
                    "annualized_rate": round(float(data.annualizedRate), 3),
                    "annualized_rate_uah": round(float(data.annualizedRate) * uah_price, 3),
                    "investment": round(float(data.investment), 3),
                    "investment_uah": round(float(data.investment) * uah_price, 3),
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
                },
                "hint": {
                    "algo_id": "Номер",
                    "annualized_rate": "Розрахунковий річний дохід (USD)",
                    "annualized_rate_uah": "Розрахунковий річний дохід (UAH)",
                    "investment": "Сума депозиту (USD)",
                    "investment_uah": "Сума депозиту (UAH)",
                    "profit": "Отриманий дохід (USD)",
                    "profit_uah": "Отриманий дохід (UAH)",
                    "float_profit": "Поточний стан (USD)",
                    "float_profit_uah": "Поточний стан (UAH)",
                    "total_price": "Ціна гріду (USD)",
                    "total_price_uah": "Ціна гріду (UAH)",
                    "run-price": "Ціна на запуску (USD)",
                    "run-price_uah": "Ціна на запуску (UAH)",
                    "trades_num": "Кількість торгів",
                    "arbitrages_num": "Кількість арбітражів",
                    "created_at_utc": "Дата створення",
                    "instance_id": "Біржа",
                    "instance_type": "Екземпляр",
                    "order_type": "Вид доходу",
                }
            })
        except Exception as e:
            return jsonify({"success": False, "exception": str(e)})
