from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Datum(BaseModel):
    instType: str
    instId: str
    last: str
    lastSz: str
    askPx: str
    askSz: str
    bidPx: str
    bidSz: str
    open24h: str
    high24h: str
    low24h: str
    volCcy24h: str
    vol24h: str
    ts: str
    sodUtc0: str
    sodUtc8: str


class Model(BaseModel):
    code: str
    msg: str
    data: List[Datum]
