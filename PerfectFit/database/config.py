import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def get_session():
    return db.session


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1234@localhost/perfectfit'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('FLASH_SECRET_KEY')
