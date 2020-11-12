from flask.views import MethodView
from flask import jsonify, request, Blueprint
from database import db
from marshmallow import ValidationError
from services.statistic import StatisticService, IncorrectData
from scheme.statistic import statistic_scheme
from flask_cors import cross_origin
from auth_required import auth_required
from services.auth import AuthService, NotExistToken
import jwt
bp = Blueprint('statistic', __name__)


class NewsView(MethodView):
    """
    class for registering and gets a user
    """
    @cross_origin(supports_credentials=True)
    @auth_required
    def post(self, user_id):
        request_json = request.json

        service = StatisticService(db.connection)
        service.save_event(request_json, user_id)

        return jsonify(''), 200

    @cross_origin(supports_credentials=True)
    def get(self):
        request_args = request.args
        try:
            statistic = statistic_scheme.load(request_args)
        except ValidationError as val_er:
            return jsonify(val_er.messages), 400
        service = StatisticService(db.connection)
        try:
            return_statistic = service.get_event(statistic)
        except IncorrectData as incorrect_err:
            return jsonify(incorrect_err.message), 400
        return jsonify(return_statistic), 200


bp.add_url_rule('', view_func=NewsView.as_view('statistic'))
