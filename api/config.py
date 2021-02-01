import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """ A class to manage and set Flask configuration variables. """

    API_URL_PREFIX = '/'

    # Secret Keys
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'do-not-use-in-production'

    # JWT Config
    # JWT_SECRET_KEY = 'Individually set JWT SECRET KEY or defaults to SECRET KEY.
    JWT_BLACKLIST_ENABLED = True  # Enable blacklist users.
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']  # Check both access and refresh tokens.

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
