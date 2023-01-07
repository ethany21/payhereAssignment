from fastapi import FastAPI
from src.router import LedgerApi, UserLoginApi

app = FastAPI()

app.include_router(LedgerApi.router)
app.include_router(UserLoginApi.router)

