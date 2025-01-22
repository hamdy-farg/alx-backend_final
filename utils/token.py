import os

from flask_smorest import abort
from itsdangerous import URLSafeSerializer

from extension import mail


class Token:
    @staticmethod
    def generate_token(email: str) -> str:
        serializer = URLSafeSerializer(os.getenv("JWT_SECRET_KEY"))
        return serializer.dumps(email, salt=os.getenv("SECURITY_PASSWORD_SALT"))

    @staticmethod
    def confirm_token(token, expireation=300):
        serializer = URLSafeSerializer(os.getenv("JWT_SECRET_KEY"))
        try:
            email = serializer.loads(
                token, salt=os.getenv("SECURITY_PASSWORD_SALT"), max_age=expireation
            )
            return email
        except Exception as e:
            abort(403, message=str(e))
