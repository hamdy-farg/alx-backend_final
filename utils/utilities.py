import os

from firebase_admin import messaging
from flask_mail import Mail, Message

from app import app
from extension import mail


class Utilities:
    def sendNotification(
        self, fcm_token: str, title: str, message: str, route: str = "/home"
    ):
        try:
            notification = messaging.Notification(
                title=title,
                body=message,
                # image="",  # URL of the image
            )
            data = {
                "route": "/details",  # Route to navigate to in Flutter
            }
            firebase_message = messaging.Message(
                notification=notification,
                data=data,  # Include the data payload
                token=fcm_token,
            )
            response = messaging.send(firebase_message)

        except Exception as e:
            print(f"error{str(e)}")

        return True

    @staticmethod
    def send_email(to, subject, template):
        try:
            print(subject, to)
            msg = Message(
                subject,
                recipients=[to],
                html=template,
                sender="noreply@flask.com",
            )
            mail.send(msg)
        except Exception as e:
            abort(400, message=str(e))
