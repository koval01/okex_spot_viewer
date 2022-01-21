from __future__ import annotations
from flask_cors import CORS
from flask_restful import Resource, Api
from flask import Flask, jsonify, render_template
import os
from time import time
from datetime import timedelta
import json
import logging
import requests_cache
from requests import get as http_get
from typing import List
from pydantic import BaseModel


class Datum(BaseModel):
    algoId: str
    annualizedRate: str
    arbitrageNum: str
    baseSz: str
    cTime: str
    cancelType: str
    ccy: str
    ctVal: str
    curBaseSz: str
    curQuoteSz: str
    floatProfit: str
    gridNum: str
    gridProfit: str
    instId: str
    instType: str
    investment: str
    last: str
    lever: str
    maxPx: str
    minPx: str
    ordId: str
    ordType: str
    pTime: str
    perMaxProfitRate: str
    perMinProfitRate: str
    pnlRatio: str
    quoteSz: str
    runPx: str
    runType: str
    singleAmt: str
    slOrderPx: str
    slTriggerPx: str
    sourceIntValue: int
    state: str
    stopResult: str
    tag: str
    tdMode: str
    totalAnnualizedRate: str
    totalPnl: str
    tpOrderPx: str
    tpTriggerPx: str
    tradeNum: str
    triggerTime: str
    uly: str


class ModelData(BaseModel):
    code: str
    data: List[Datum]
    msg: str


class OkxApi:
    def __init__(self) -> None:
        self.host = "www.okx.com"
        self.path = "priapi/v5/algo/trade/info"
        self.params = {
            "t": round(time()),
            "algoId": os.getenv("ALGO_ID")
        }
        self.headers = {
            "Authorization": os.getenv("AUTH_KEY")
        }

    def __str__(self) -> str:
        resp = http_get(
            url=f"https://{self.host}/{self.path}",
            params=self.params, headers=self.headers
        ).json()
        return json.dumps(obj=resp, indent=5)

    @staticmethod
    def short_id(id_: str) -> str:
        return f"{'*'*(len(id_)-6)}{id_[-6:]}"


class CurrencyGet:
    def __init__(self, mode: str = "USD_UAH") -> None:
        self.session = requests_cache.CachedSession(
            name = "CurrencyGet", backend = "memory", 
            expire_after = timedelta(minutes=5))
        self.host = "free.currconv.com"
        self.path = "api/v7/convert"
        self.mode = mode
        self.params = {
            "q": self.mode,
            "compact": "ultra",
            "apiKey": os.getenv("CURRENCY_API_KEY"),
        }

    def __str__(self) -> str:
        try:
            return str(self.session.get(
                url=f"https://{self.host}/{self.path}",
                params=self.params
            ).json()[self.mode])
        except Exception as e:
            logging.error("%s: %s" % (CurrencyGet.__name__, e))
            return "0"


app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

class DataJson(Resource):
    @staticmethod
    def get() -> jsonify:
        try:
            loads = json.loads(str(OkxApi()))
            data = ModelData(**loads).data[0]
            uah_price = float(f"{CurrencyGet()}")
            return jsonify({
                "success": len(loads["data"]) > 0,
                "data": {
                    "algo_id":               OkxApi().short_id(data.algoId),
                    "annualized_rate":       float(data.annualizedRate),
                    "annualized_rate_uah":   float(data.annualizedRate) * uah_price,
                    "investment":            float(data.investment),
                    "investment_uah":        float(data.investment) * uah_price,
                    "profit":                float(data.gridProfit),
                    "profit_uah":            float(data.gridProfit) * uah_price,
                    "float_profit":          float(data.floatProfit),
                    "float_profit_uah":      float(data.floatProfit) * uah_price,
                    "total_price":           float(data.totalPnl),
                    "total_price_uah":       float(data.totalPnl) * uah_price,
                    "run-price":             float(data.runPx),
                    "run-price_uah":         float(data.runPx) * uah_price,
                    "trades_num":            int(data.tradeNum),
                    "arbitrages_num":        int(data.arbitrageNum),
                    "created_at_utc":        int(data.cTime),
                    "instance_id":           str(data.instId),
                    "instance_type":         str(data.instType),
                    "order_type":            str(data.ordType),
                },
                "hint": {
                    "algo_id":               "Grid number",
                    "annualized_rate":       "Estimated Annual Income (USD)",
                    "annualized_rate_uah":   "Estimated annual income (UAH)",
                    "investment":            "Deposit amount (USD)",
                    "investment_uah":        "Deposit amount (UAH)",
                    "profit":                "Income received (USD)",
                    "profit_uah":            "Income received (UAH)",
                    "float_profit":          "Current state of the grid (USD)",
                    "float_profit_uah":      "Current state of the grid (UAH)",
                    "total_price":           "Grid Current Value (USD)",
                    "total_price_uah":       "Grid Current Value (UAH)",
                    "run-price":             "Rate at the time of launch (USD)",
                    "run-price_uah":         "Rate at the time of launch (UAH)",
                    "trades_num":            "Number of trades",
                    "arbitrages_num":        "Number of arbitrations",
                    "created_at_utc":        "The date the grid was created",
                    "instance_id":           "Exchange",
                    "instance_type":         "Instance",
                    "order_type":            "Type of income",
                }
            })
        except Exception as e:
            return jsonify({"success": False, "exception": str(e)})


api.add_resource(DataJson, '/')

if __name__ == "__main__":
    app.run()
