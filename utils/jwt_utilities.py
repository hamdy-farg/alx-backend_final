from extension import jwt
from models import UserModel
from block_list import BLOCKLIST
from models import RoleEnum
from flask import jsonify


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.query.filter(UserModel.id == identity).first()
    if user is not None:
        if user.role == RoleEnum.client:
            return {"is_admin": False}
        else:
            return {"is_admin": True}


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


...


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
    )


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payloud):
    jti = jwt_payloud["jti"]
    print(BLOCKLIST)
    return jti in BLOCKLIST
