from __future__ import annotations
from flask_cors import CORS
from flask_restful import Resource, Api
from flask import Flask, jsonify
import os
from time import time
import json
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


app = Flask(__name__)
api = Api(app)
CORS(app)

class DataReturn(Resource):
    @staticmethod
    def get() -> jsonify:
        data = ModelData(**json.loads(str(OkxApi()))).data[0]
        return jsonify({
            "data": {
                "algo_id": OkxApi().short_id(data.algoId),
                "instance_id": data.instId,
                "instance_type": data.instType,
                "order_type": data.ordType,
                "investment": float(data.investment),
                "profit": float(data.gridProfit),
                "trades_num": int(data.tradeNum),
                "arbitrages_num": int(data.arbitrageNum),
                "created_at_utc": int(data.cTime),
            }
        })


api.add_resource(DataReturn, '/')

if __name__ == "__main__":
    app.run()
