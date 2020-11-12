"""
module with business logic for user registration and getting user
:classes:
UserService - class for registering and getting a user
"""
from models import UserModel
from werkzeug.security import generate_password_hash
from exception import ServiceError
from entities.user import UserCreate, BaseUser


class UserError(ServiceError):
    """
    class for inherit exception
    """
    service = 'user'


class ThisEmailAlreadyUse(UserError):
    """
    class with conflict error email
    """
    message = {"answer": "Данный email уже используется"}


class UserService:
    """
    UserService - class for registering and getting a user
    """
    def __init__(self, session):
        """
        class constructor
        :param session: connect to db
        """
        self.session = session

    def create_user(self, user: UserCreate) -> BaseUser:
        """
        registering user
        :param user: dataclass with data for auth user
        :return: dataclass user
        """
        old_user = (self.session.query(UserModel).filter
                    (UserModel.login == user.login).first())

        if old_user is not None:
            raise ThisEmailAlreadyUse()

        password_hash = generate_password_hash(user.password)
        new_user = UserModel(login=user.login, password=password_hash, role="user")

        self.session.add(new_user)
        self.session.commit()
        return self.get_user(new_user.as_dict().get('id'))

    def get_user(self, user_id: int) -> BaseUser:
        """
        getting user
        :param user_id: id user in session
        :return: dataclass user
        """
        data_user = (self.session.query(UserModel).filter
                     (UserModel.id == user_id).first())

        data_user = data_user.as_dict()
        return BaseUser(login=data_user.get('login'))
