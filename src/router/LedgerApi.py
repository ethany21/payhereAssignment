from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from starlette import status

from src.auth.Auth_Bearer import JWTBearer
from src.config.Connection import get_db
from src.dto.LedgerDto import ResponseLedger, RequestLedgerCreate, RequestLedgerUpdate
from src.entity.Model import UserLogin, Ledger
from src.service.LedgerService import LedgerService
from src.util.Util import get_current_user

router = APIRouter(
    prefix="/ledger",
    tags=["ledger"],
    dependencies=[Depends(JWTBearer())]
)


@router.post("/", response_model=ResponseLedger,
             status_code=status.HTTP_201_CREATED)
def insert_ledger(ledger: RequestLedgerCreate, db: Session = Depends(get_db),
                  current_user: UserLogin = Depends(get_current_user)):
    if not ledger.price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing value in request body: price")
    if not ledger.memo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing value in request body: memo")

    try:
        return LedgerService(db).create_ledger(ledger=ledger, current_user=current_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())


@router.get("/ledgers", response_model=List[ResponseLedger], status_code=status.HTTP_200_OK)
def get_ledgers(db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user)):
    try:
        selected_ledgers = LedgerService(db).get_all_ledgers(current_user=current_user)
        if not selected_ledgers:
            raise Exception("no one found")
        return selected_ledgers
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())


@router.get('/{ledger_id}', response_model=ResponseLedger, status_code=status.HTTP_200_OK)
def get_ledger(ledger_id: int, db: Session = Depends(get_db), current_user: UserLogin = Depends(get_current_user)):
    try:
        return LedgerService(db).get_ledger(ledger_id=ledger_id, current_user=current_user)
    except NoResultFound:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Selected wrong ledger id in current user")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())


@router.patch("/{ledger_id}", status_code=status.HTTP_200_OK)
def update_ledger(ledger_id: int, updated_ledger: RequestLedgerUpdate, db: Session = Depends(get_db),
                  current_user: UserLogin = Depends(get_current_user)
                  ):
    try:
        LedgerService(db).update_ledger(ledger_id=ledger_id, current_user=current_user, updated_ledger=updated_ledger)

    except NoResultFound:
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Selected wrong ledger id in current user")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())


@router.delete("/{ledger_id}", status_code=status.HTTP_200_OK)
def delete_ledger(ledger_id: int, db: Session = Depends(get_db),
                  current_user: UserLogin = Depends(get_current_user)):
    try:
        LedgerService(db).delete_leger(ledger_id=ledger_id, current_user=current_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())
