from flask.views import MethodView
from flask import Blueprint
from database import db
from services.account import AccountService
from flask_cors import cross_origin
from flask import render_template
from auth_required import auth_required

bp = Blueprint('account', __name__)


class UserView(MethodView):
    """
    cтраница аккаунта
    """
    @cross_origin(supports_credentials=True)
    @auth_required
    def get(self, user_id):
        # отдаем тут страницу аккаунта
        service = AccountService(db.connection)
        user_role = service.get_user_role(user_id)
        print(user_role, 'role user print')
        return render_template("account.html", user=user_role)




bp.add_url_rule('', view_func=UserView.as_view('account'))