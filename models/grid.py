from __future__ import annotations

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
