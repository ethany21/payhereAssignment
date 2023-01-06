from pydantic import BaseModel


class RequestLedger(BaseModel):
    price: int
    memo: str


class ResponseLedger(BaseModel):
    id: int
    price: int
    memo: str

    class Config:
        orm_mode = True
