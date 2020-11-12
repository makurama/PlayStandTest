from functools import wraps
from flask import session, request
from flask.sessions import SecureCookieSession

from models import UserModel
from database import db
import jwt

def auth_required(view_func):
    """
    decorator to check if the user is authorized
    :param view_func: view func
    :return: all that was accepted
    """
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            return {"answer": "Авторизуйтесь"}, 401
        user_data = (db.connection.query(UserModel).filter
                     (UserModel.id == user_id).first())
        if user_data is None:
            return {"answer": "Данного пользователя не сущесвует"}, 404
        db.close_db(exception=None)
        return view_func(*args, **kwargs, user_id=user_id)
    return wrapper