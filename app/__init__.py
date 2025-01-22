import os
import json
from dotenv import load_dotenv
from resource.booked import blp as BookedBluePrint
from resource.notifcation import blp as notifcationBluePrint
from resource.room import blp as RoomBluePrint
from resource.user import blp as UserBluePrint
from resource.work_space import blp as WorkSpaceBluePrint
from resource.verification import blp as VerificationBluePrint
import firebase_admin
from firebase_admin import credentials
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_smorest import Api

from extension import db, jwt, mail, socketio  # Import extensions from extensions.py
from models import RoleEnum, StatusEnum, UserModel
from flask_socketio import SocketIO


#################
from utils.configuration import Config


def create_app():
    """ " create app
    create all flask app config
    """

    app = Flask(__name__)
    # flask smores configuration
    app.config.from_object(Config)
    mail.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app=app)
    api = Api(app)
    app.has_initialized = False
    app.app_context().push()
    #

    api.register_blueprint(notifcationBluePrint)
    api.register_blueprint(UserBluePrint)
    api.register_blueprint(WorkSpaceBluePrint)
    api.register_blueprint(RoomBluePrint)
    api.register_blueprint(BookedBluePrint)
    api.register_blueprint(VerificationBluePrint)

    def create_tables():
        if not app.has_initialized:
            app.has_initialized = True
            db.create_all()

    create_tables()

    return app


##########

######

load_dotenv("./.env")
FIREBASE_PRIVATE_KEY = os.getenv("FIREBASE_PRIVATE_KEY")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
FIREBASE_CLIENT_EMAIL = os.getenv("FIREBASE_CLIENT_EMAIL")
FIREBASE_CLIENT_ID = os.getenv("FIREBASE_CLIENT_ID")
FIREBASE_AUTH_URI = os.getenv("FIREBASE_AUTH_URI")
FIREBASE_TOKEN_URI = os.getenv("FIREBASE_TOKEN_URI")
FIREBASE_AUTH_PROVIDER_X509_CERT_URL = os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL")
FIREBASE_CLIENT_X509_CERT_URL = os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
FIREBASE_UNIVERSE_DOMAIN = os.getenv("FIREBASE_UNIVERSE_DOMAIN")
app = create_app()
###########
print(os.getenv("FIREBASE_CONSOLE_SECRET"))
firebase_cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": FIREBASE_PROJECT_ID,
        "private_key_id": "f553eb33d483b67813e823a95f8c9949e8e12645",
        "private_key": FIREBASE_PRIVATE_KEY,
        "client_email": FIREBASE_CLIENT_EMAIL,
        "client_id": FIREBASE_CLIENT_ID,
        "auth_uri": FIREBASE_AUTH_URI,
        "token_uri": FIREBASE_TOKEN_URI,
        "auth_provider_x509_cert_url": FIREBASE_AUTH_PROVIDER_X509_CERT_URL,
        "client_x509_cert_url": FIREBASE_CLIENT_X509_CERT_URL,
        "universe_domain": FIREBASE_UNIVERSE_DOMAIN,
    }
)

firebase_app = firebase_admin.initialize_app(firebase_cred)
migrate = Migrate(app, db)  # Initialize Flask-Migrate
# cors = CORS(app, resources={r"/*": {"origins": "*"}})


#####################
from utils.jwt_utilities import (
    add_claims_to_jwt,
    expired_token_callback,
    invalid_token_callback,
    missing_token_callback,
    token_not_fresh_callback,
    check_if_token_in_blocklist,
)
