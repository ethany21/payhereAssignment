import jwt
from decouple import config
from typing import Dict
import time

from passlib.context import CryptContext

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")
password_context = CryptContext(schemes=['sha256_crypt'], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 1800
    }

    return token_response(jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM))


def decodeJWT(token: str) -> dict:
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decode_token if decode_token["expires"] >= time.time() else None
    except:
        return {}
