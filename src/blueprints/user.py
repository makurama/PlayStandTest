from marshmallow import ValidationError
import scheme.user
from flask import (
    Blueprint,
    request,
    jsonify
)
from flask.views import MethodView
from database import db
from services.user import UserService, ThisEmailAlreadyUse
bp = Blueprint('user', __name__)


class UserView(MethodView):
    """
    Создание аккаутна
    """
    def post(self):
        request_json = request.json
        try:
            user = scheme.user.user_schema.load(request_json)
        except ValidationError as ValidEr:
            return jsonify(ValidEr.messages), 400
        service = UserService(db.connection)
        try:
            user = service.create_user(user=user)
        except ThisEmailAlreadyUse as email_er:
            return email_er.message, 400
        return jsonify(scheme.user.get_user_schema.dump(user)), 201


bp.add_url_rule('', view_func=UserView.as_view('user'))