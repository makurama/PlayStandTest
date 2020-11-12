import os


class Config:
    DB_CONNECTION = os.getenv('DB_CONNECTION', 'sqlite:///database.db')
    SECRET_KEY = os.getenv('SECRET_KEY').encode()
    SESSION_TYPE = 'filesystem'
