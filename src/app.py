"""
module with application entry point
"""
from flask import Flask
from flask_cors import CORS
from database import db
from blueprints.user import bp as bp_user
from blueprints.auth import bp as bp_auth
from blueprints.news import bp as bp_news
from blueprints.account import bp as bp_account
from blueprints.statistic import bp as bp_statistic
from blueprints.index import bp as bp_index
import datetime
from flask_session import Session

def create_app():
    """
    entry point
    """
    app = Flask(__name__)
    app.config.from_object('config.Config')
    Session(app)
    CORS(app)
    app.register_blueprint(bp_user, url_prefix='/user')
    app.register_blueprint(bp_auth, url_prefix='/auth')
    app.register_blueprint(bp_news, url_prefix='/news')
    app.register_blueprint(bp_account, url_prefix='/account')
    app.register_blueprint(bp_statistic, url_prefix='/statistic')
    app.register_blueprint(bp_index, url_prefix='/')
    db.init_app(app)
    return app
