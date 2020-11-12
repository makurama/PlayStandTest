from flask.views import MethodView
from flask import jsonify, request, Blueprint, session
from marshmallow import ValidationError
from database import db
from services.account import AccountService
from flask_cors import CORS, cross_origin
from services.auth import AuthService, NotExistToken
import jwt
from flask import render_template

bp = Blueprint('/', __name__)


class UserView(MethodView):
    """
    class for registering and gets a user
    """
    @cross_origin(supports_credentials=True)
    def get(self):
        return render_template("index.html")



bp.add_url_rule('', view_func=UserView.as_view('/'))