# Base configuration to be used on running server

"""
Note: Unless you are working on the server itself, you will not be able to run 
it with a Config object. You must use a DevelopmentConfig or TestConfig.
"""
import os
from secrets import MYSQL_DB, SECRET_KEY_VAR, CSRF_SESSION_KEY_VAR, RECAPTCHA_PUBLIC_KEY_VAR, RECAPTCHA_PRIVATE_KEY_VAR, GOOGLE_CLIENT_ID_VAR, GOOGLE_CLIENT_SECRET_VAR, WEPAY_ACC_TOK_VAR
_basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    Testing = False

    ADMINS = frozenset(['acm.at.ucr+webmaster@gmail.com'])

    SQLALCHEMY_DATABASE_URI = MYSQL_DB
    DATABASE_CONNECT_OPTIONS = {}

    THREADS_PER_PAGE = 8

    CSRF_ENABLED = True
    RECAPTCHA_USE_SSL = False
    RECAPTCHA_OPTIONS = {'theme': 'white'}

    # Giving server defined configuration default values.
    SECRET_KEY = None
    CSRF_SESSION_KEY = None
    RECAPTCHA_PUBLIC_KEY = None
    RECAPTCHA_PRIVATE_KEY = None
    GOOGLE_CLIENT_ID = None
    GOOGLE_CLIENT_SECRET = None
    HOST_URL = None
    WEPAY_ACCT_ID = None
    WEPAY_ACC_TOK = None
    WEPAY_IN_PROD = None

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = SECRET_KEY_VAR

    CSRF_SESSION_KEY = CSRF_SESSION_KEY_VAR
    RECAPTCHA_PUBLIC_KEY = RECAPTCHA_PUBLIC_KEY_VAR
    RECAPTCHA_PRIVATE_KEY = RECAPTCHA_PRIVATE_KEY_VAR

    GOOGLE_CLIENT_ID = GOOGLE_CLIENT_ID_VAR
    GOOGLE_CLIENT_SECRET = GOOGLE_CLIENT_SECRET_VAR

    HOST_URL = 'http://localhost:5000'

    WEPAY_ACCT_ID = 319493
    WEPAY_ACC_TOK = WEPAY_ACC_TOK_VAR
    WEPAY_IN_PROD = False

class TestingConfig(DevelopmentConfig):
    DEBUG = False
    TESTING = True
    CSRF_ENABLED = False
    WTF_CSRF_CHECK_DEFAULT = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'tests/test.db')
