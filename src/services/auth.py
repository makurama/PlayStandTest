"""
module with business logic for user authorization
:classes:
AuthService - this class allows produce authorization
"""
from models import UserModel
from werkzeug.security import check_password_hash
from exception import ServiceError
from entities.auth import Auth
import jwt
from datetime import datetime, timedelta
from config import Config
from typing import Tuple

class AuthError(ServiceError):
    """
    class error auth for inherit
    """
    service = 'auth'


class NotExistToken(ServiceError):
    message = {"answer": "Вы не авторизованны"}


class UserNotFoundOrInvalidData(AuthError):
    """
    class for exception, Invalid data or user does not exist
    """
    message = {"answer": "Данного пользователя не существует "
                         "или введены неверные данные"}


class AuthService:

    """
    AuthService - this class allows produce authorization
    """
    def __init__(self, session):
        """
        class constructor
        :param session: connect to db
        """
        self.session = session

    def authorization(self, user: Auth) -> Tuple[int, bytes]:
        """
        method accepts dateclass and authorize user
        :param user: authorization data
        :return: user id
        """
        user_data = (self.session.query(UserModel).filter
                     (UserModel.login == user.login).first())

        if (user_data is None):
            raise UserNotFoundOrInvalidData()

        if check_password_hash(user_data.password, user.password):
            return user_data.id
        else:
            raise UserNotFoundOrInvalidData()
