from models import UserModel


class AccountService:
    """
    Тут просто отдаем подготовленный шаблон аккаунта
    """
    def __init__(self, session):
        self.session = session

    def get_user_role(self, user_id):
        query = (
            self.session.query(UserModel)
            .filter(UserModel.id == user_id).first()
        )
        return query.as_dict().get('role')

