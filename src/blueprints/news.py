from flask.views import MethodView
from flask import jsonify, request, Blueprint
from marshmallow import ValidationError
from database import db
from services.news import NewsService, NoNews
from scheme.news import news_scheme
from auth_required import auth_required
from flask_cors import cross_origin

bp = Blueprint('news', __name__)


class NewsView(MethodView):
    """
    Новости
    """
    @cross_origin(supports_credentials=True)
    @auth_required
    def get(self, user_id):
        request_args = request.args

        try:
            news = news_scheme.load(request_args)
        except ValidationError as val_er:
            return jsonify(val_er.messages), 400
        service = NewsService(db.connection)
        try:
            return_news = service.get_news(news)
        except NoNews:
            return NoNews.message, 404

        return jsonify(return_news), 200


bp.add_url_rule('', view_func=NewsView.as_view('news'))