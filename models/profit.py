from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Datum(BaseModel):
    cTime: str
    pnlRatio: str
    profitNum: str
    timeUnit: str
    totalPnl: str


class Model(BaseModel):
    code: str
    data: List[Datum]
    msg: str
