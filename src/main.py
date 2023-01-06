from typing import List
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session
from starlette import status

from src.auth.Auth_Bearer import JWTBearer
from src.auth.Auth_Handler import get_hashed_password, signJWT, verify_password
from src.config.Connection import get_db
from src.dto.LedgerDto import RequestLedgerCreate, ResponseLedger, RequestLedgerUpdate
from src.dto.UserLoginDto import RequestUserLogin
from src.entity.Model import Ledger, UserLogin
from src.util.Util import get_current_user

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
def insert_ledger(ledger: RequestLedgerCreate, db: Session = Depends(get_db),
                  current_user: UserLogin = Depends(get_current_user)):
    if not ledger.price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing value in request body: price")
    if not ledger.memo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing value in request body: memo")

    try:
        ledger = Ledger(
            price=ledger.price,
            memo=ledger.memo,
            user=current_user
        )
        db.add(ledger)
        db.commit()
        return ledger
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())


@app.get("/ledgers", tags=["ledger"], response_model=List[ResponseLedger], dependencies=[Depends(JWTBearer())])
def get_ledgers(db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user)):
    try:
        selected_ledgers = db.query(Ledger).filter(Ledger.user_id == current_user.id).all()
        if not selected_ledgers:
            raise Exception("no one found")
        return selected_ledgers
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())


@app.get('/ledger/{ledger_id}', tags=["ledger"], response_model=ResponseLedger, dependencies=[Depends(JWTBearer())])
def get_ledger(ledger_id: int, db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user)):
    try:
        selected_ledger = db.query(Ledger).filter(
            Ledger.id == ledger_id
        ).filter(Ledger.user_id == current_user.id).one()
        return selected_ledger
    except NoResultFound:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Selected wrong ledger id in current user")
    except Exception as e:
        logger.error("error: ", e.__str__())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())


@app.patch("/ledger/{ledger_id}", tags=["ledger"], dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
def update_ledger(ledger_id: int, updated_ledger: RequestLedgerUpdate, db: Session = Depends(get_db),
                  current_user: UserLogin = Depends(get_current_user)
                  ):
    try:
        selected_ledger = db.query(Ledger).filter(
            Ledger.id == ledger_id
        ).filter(Ledger.user_id == current_user.id).one()

        if updated_ledger.memo:
            selected_ledger.memo = updated_ledger.memo
        if updated_ledger.price:
            selected_ledger.price = updated_ledger.price

        db.add(selected_ledger)
        db.commit()

    except NoResultFound:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Selected wrong ledger id in current user")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())


@app.delete("/ledger/{ledger_id}", tags=["ledger"], dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK)
def delete_ledger(ledger_id: int, db: Session = Depends(get_db),
                  current_user: UserLogin = Depends(get_current_user)):
    try:
        db.query(Ledger).filter(Ledger.id == ledger_id) \
            .filter(
            Ledger.user_id == current_user.id
        ).delete()
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())


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
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())


@app.post("/user/login", tags=["user"])
def login_user(user: RequestUserLogin, db: Session = Depends(get_db)):
    searched_user = db.query(UserLogin).filter(UserLogin.email == user.email).one()
    if not searched_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    if not verify_password(user.password, searched_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    return signJWT(searched_user.email)
