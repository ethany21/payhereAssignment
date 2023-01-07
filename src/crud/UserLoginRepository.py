import logging

from sqlalchemy.orm import Session

from src.dto.UserLoginDto import RequestUserLogin
from src.entity.Model import UserLogin
from src.interface.Interface import AppRepository

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class UserLoginRepository(AppRepository):

    def get_login_user(self, user_email: str):
        return self.db.query(UserLogin).filter(UserLogin.email == user_email).one()

    def create_user(self, user: RequestUserLogin):
        new_user = UserLogin(**user.dict())
        self.db.add(new_user)
        self.db.commit()
