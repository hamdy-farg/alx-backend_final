import os


class Config(object):
    PROPAGATE_EXCEPTION = True
    # flask smorest configuration

    API_TITLE = "UDEMY FLASK TEST"
    API_VERSION = "v1.0"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "hi")
    SQLALCHEMY_DATABASE_URI = "mysql://root:QoHGirHdGGWGycizxspQJFiGkXRRmGcm@mysql.railway.internal:3306/railway"
    # "mysql-production-632e.up.railway.app"
    #  "mysql+mysqlconnector://root:0000@127.0.0.1:3306/bankdb1"

    # "mysql://avnadmin:AVNS_ubxukWZBkNZDpbXVqm4@mysql-9922e3a-farghamdy72-61e3.b.aivencloud.com:25133/defaultdb2"
    SQLALCHEMY_TRACK_MODIFICATION = False
    # JWT config
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "hi")
    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     'connect_args': {
    #         'ssl': {
    #             'ssl_ca': "C:\\Users\\spider\\Desktop\\IBM_BACKEND_PROJECT\\ca.pem"
    #         }
    #     }
    # }
    # email send configuration
    MAIL_DEFAULT_SENDER = os.getenv("EMAIL_USER")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = os.getenv("EMAIL_USER")
    MAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    SERVER_NAME = os.getenv("SERVER_NAME", "127.0.0.1:5000")
