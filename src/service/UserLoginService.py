from src.auth.Auth_Handler import get_hashed_password, signJWT
from src.crud.UserLoginRepository import UserLoginRepository
from src.dto.UserLoginDto import RequestUserLogin
from src.interface.Interface import AppService


class UserLoginService(AppService):

    def signup_user(self, user: RequestUserLogin):
        user.password = get_hashed_password(user.password)
        signup_user = UserLoginRepository(self.db).create_user(user=user)
        return signJWT(signup_user.email)

    def get_login_user(self, user: RequestUserLogin):
        return UserLoginRepository(self.db).get_login_user(user_email=user.email)
