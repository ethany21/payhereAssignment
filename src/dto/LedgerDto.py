from typing import Optional

from pydantic import BaseModel


class RequestLedgerCreate(BaseModel):
    price: int
    memo: str


class RequestLedgerUpdate(BaseModel):
    price: Optional[int]
    memo: Optional[str]


class ResponseLedger(BaseModel):
    id: int
    price: int
    memo: str

    class Config:
        orm_mode = True
