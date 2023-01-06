from pydantic import BaseModel


class RequestUserLogin(BaseModel):
    email: str
    password: str


class ResponseUserLogin(BaseModel):
    id: int
    email: str
    password: str

    class Config:
        orm_mode = True
