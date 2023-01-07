from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from src.auth.Auth_Bearer import JWTBearer
from src.auth.Auth_Handler import get_hashed_password, signJWT, verify_password
from src.config.Connection import get_db
from src.dto.UserLoginDto import RequestUserLogin
from src.entity.Model import UserLogin
from src.service.UserLoginService import UserLoginService

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/signup")
def signup_user(user: RequestUserLogin, db: Session = Depends(get_db)):
    try:
        return UserLoginService(db).signup_user(user=user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.__str__())


@router.post("/login")
def login_user(user: RequestUserLogin, db: Session = Depends(get_db)):
    searched_user = UserLoginService(db).get_login_user(user=user)
    if not searched_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    if not verify_password(user.password, searched_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    return signJWT(searched_user.email)
