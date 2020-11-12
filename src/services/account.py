from models import UserModel
from flask import jsonify, request, Blueprint
from sqlalchemy import func, and_, between
from datetime import datetime
from exception import ServiceError
from typing import List
import pars_newsru
import pars_chelru
import time


class AccountService:
    def __init__(self, session):
        self.session = session

    def get_user_role(self, user_id):
        query = (
            self.session.query(UserModel)
            .filter(UserModel.id == user_id).first()
        )
        return query.as_dict().get('role')

