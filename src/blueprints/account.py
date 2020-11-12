from flask.views import MethodView
from flask import jsonify, request, Blueprint, session
from marshmallow import ValidationError
from database import db
from services.account import AccountService
from flask_cors import CORS, cross_origin
from services.auth import AuthService, NotExistToken
import jwt
from flask import render_template
from auth_required import auth_required

bp = Blueprint('account', __name__)


class UserView(MethodView):
    """
    class for registering and gets a user
    """
    @cross_origin(supports_credentials=True)
    @auth_required
    def get(self, user_id):
        # и страницу админа или юзера ему отдавать
        service = AccountService(db.connection)
        user_role = service.get_user_role(user_id)
        print(user_role, 'role user print')
        return render_template("account.html")
        # if user_role == 'admin':
        #     return render_template("account.html")
        # else:
        #     return render_template("account.html")




bp.add_url_rule('', view_func=UserView.as_view('account'))