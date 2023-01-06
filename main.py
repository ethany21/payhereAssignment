from typing import List
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from auth.Auth_Bearer import JWTBearer
from auth.Auth_Handler import get_hashed_password, signJWT, verify_password, JWT_SECRET, JWT_ALGORITHM
from config.Connection import get_db
from dto.LedgerDto import RequestLedger, ResponseLedger
from dto.UserLoginDto import RequestUserLogin
from entity.Model import Ledger, UserLogin
from util.Util import get_current_user

app = FastAPI()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


@app.post("/ledger", tags=["ledger"], response_model=ResponseLedger, dependencies=[Depends(JWTBearer())],
          status_code=status.HTTP_201_CREATED)
def insert_ledger(ledger: RequestLedger, db: Session = Depends(get_db),
                  current_user: UserLogin = Depends(get_current_user)):

    ledger = Ledger(
        price=ledger.price,
        memo=ledger.memo,
        user=current_user
    )
    db.add(ledger)
    db.commit()
    return ledger


@app.get("/ledgers", tags=["ledger"], response_model=List[ResponseLedger], dependencies=[Depends(JWTBearer())])
def get_ledgers(db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user)):
    return db.query(Ledger).filter(Ledger.user_id == current_user.id).all()


@app.patch("/ledger", tags=["ledger"], dependencies=[Depends(JWTBearer())])
def update_ledger(db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user)):
    pass


@app.post("/user/signup", tags=["user"])
def create_user(user: RequestUserLogin, db: Session = Depends(get_db)):
    try:
        user.password = get_hashed_password(user.password)
        new_user = UserLogin(**user.dict())
        db.add(new_user)
        db.commit()
        return signJWT(new_user.email)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist")


@app.post("/user/login", tags=["user"])
def login_user(user: RequestUserLogin, db: Session = Depends(get_db)):
    searched_user = db.query(UserLogin).filter(UserLogin.email == user.email).one()
    if not searched_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    if not verify_password(user.password, searched_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    return signJWT(searched_user.email)
