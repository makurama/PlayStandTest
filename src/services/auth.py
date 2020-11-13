"""
module with business logic for user authorization
:classes:
AuthService - this class allows produce authorization
"""
from models import UserModel
from werkzeug.security import check_password_hash
from exception import ServiceError
from entities.auth import Auth
from typing import Tuple

class AuthError(ServiceError):
    """
    class error auth for inherit
    """
    service = 'auth'


class NotExistToken(ServiceError):
    message = {"answer": "Вы не авторизованны"}


class UserNotFoundOrInvalidData(AuthError):
    message = {"answer": "Данного пользователя не существует "
                         "или введены неверные данные"}


class AuthService:
    def __init__(self, session):
        self.session = session

    def authorization(self, user: Auth) -> Tuple[int, bytes]:
        user_data = (self.session.query(UserModel).filter
                     (UserModel.login == user.login).first())

        if (user_data is None):
            raise UserNotFoundOrInvalidData()

        if check_password_hash(user_data.password, user.password):
            return user_data.id
        else:
            raise UserNotFoundOrInvalidData()
