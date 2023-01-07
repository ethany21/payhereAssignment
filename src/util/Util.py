import jwt
from fastapi import Depends, HTTPException
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette import status

from src.auth.Auth_Bearer import JWTBearer
from src.auth.Auth_Handler import JWT_SECRET, JWT_ALGORITHM
from src.config.Connection import get_db
from src.entity.Model import UserLogin


def get_current_user(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_email: str = payload.get("user_id")
        if not user_email:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    else:
        user = db.query(UserLogin).filter(UserLogin.email == user_email).one()
        if not user:
            raise credentials_exception
        return user


def check_email(email: str):
    import re
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if not (re.fullmatch(regex, email)):
        return False

    return True
