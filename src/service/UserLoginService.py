from src.auth.Auth_Handler import get_hashed_password, signJWT
from src.crud.UserLoginRepository import UserLoginRepository
from src.dto.UserLoginDto import RequestUserLogin
from src.exception.CustomException import InvalidEmailException
from src.interface.Interface import AppService
from src.util.Util import check_email


class UserLoginService(AppService):

    def signup_user(self, user: RequestUserLogin):
        if not check_email(email=user.email):
            raise InvalidEmailException
        user.password = get_hashed_password(user.password)
        signup_user = UserLoginRepository(self.db).create_user(user=user)
        return signJWT(signup_user.email)

    def get_login_user(self, user: RequestUserLogin):
        return UserLoginRepository(self.db).get_login_user(user_email=user.email)
