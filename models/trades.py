from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class Datum(BaseModel):
    groupId: Optional[str] = None
    totalPnl: Optional[str] = None
    tradeTime: Optional[str] = None
    tradeUTime: Optional[str] = None


class Model(BaseModel):
    code: str
    data: List[Datum]
    msg: Optional[str] = None
