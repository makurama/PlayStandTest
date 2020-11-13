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
    message = {"answer": "Данный email уже используется"}


class UserService:
    def __init__(self, session):
        self.session = session

    def create_user(self, user: UserCreate) -> BaseUser:
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
        data_user = (self.session.query(UserModel).filter
                     (UserModel.id == user_id).first())

        data_user = data_user.as_dict()
        return BaseUser(login=data_user.get('login'))
