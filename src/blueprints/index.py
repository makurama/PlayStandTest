from flask.views import MethodView
from flask import Blueprint, session
from flask_cors import cross_origin
from flask import render_template

bp = Blueprint('/', __name__)


class UserView(MethodView):
    """
    Загрузка главной страницы сайта
    """
    @cross_origin(supports_credentials=True)
    def get(self):

        if session.get('user_id'):# т.к. фляга сама не умеет сессию убивать, я тут её киляю
            session['user_id'] = None

        return render_template("index.html")


bp.add_url_rule('', view_func=UserView.as_view('/'))