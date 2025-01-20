from datetime import datetime

from firebase_admin import messaging
from flask import render_template, request, send_file, url_for
from flask.views import MethodView
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort

from models.enum import RoleEnum, StatusEnum
from models.user import UserModel
from schema import (
    NotificationListSchema,
    PlainNotificationSchema,
    PlainNotificationSubscribeSchema,
    SuccessSchema,
)
from utils import Token
from utils.utilities import Utilities

blp = Blueprint("Notification", "notification", description="CRUD on notification")


@blp.route("/notification")
class SubscribeNotification(MethodView):
    @jwt_required()
    @blp.arguments(PlainNotificationSubscribeSchema, location="form")
    @blp.response(200, SuccessSchema)
    def post(self, data):
        user_id = get_jwt_identity()
        fcm_token = data.get("fcm_token")
        role = data.get("role")
        user = UserModel.query.filter(UserModel.id == user_id).first()
        if user == None:
            abort(401, message="user is not found")
        try:
            responce = messaging.subscribe_to_topic(
                [fcm_token], "admin" if (role == "admin") else "client"
            )
            user.update(fcm_token=fcm_token)
            user.save()
        except Exception as e:
            abort(401, message=str(e))
        return {"code": 200, "message": "user register successfully", "success": True}
