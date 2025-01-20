from utils import Token
from utils.utilities import Utilities
from models import UserModel
from flask_smorest import abort, Blueprint
from flask import render_template, url_for
from schema import SuccessSchema
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask.views import MethodView

blp = Blueprint(
    "Verification",
    "verification",
    description="Some operation on how to verify your email address",
)


@blp.route("/confirm")
class VerifyEmail(MethodView):
    @jwt_required()
    @blp.response(200, SuccessSchema)
    def post(self):
        user_id = get_jwt_identity()
        user = UserModel.query.filter(UserModel.id == user_id).first()
        if user == None:
            abort(404, message="user not found")
        token = Token.generate_token(user.email_address)
        confirm_url = url_for("Verification.Confirmation", token=token, _external=True)
        html = render_template("confirm_email.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        Utilities.send_email(user.email_address, subject, html)
        return {"code": 200, "message": "the code sent successfuly", "success": True}


@blp.route("/confirm/<token>")
class Confirmation(MethodView):
    def get(self, token):
        email = Token.confirm_token(token)
        user = UserModel.query.filter(UserModel.email_address == email).first()
        if user == None:
            abort(404, message="user not found")
        if user.is_confirmed == True:
            return render_template("is_confirmed_before.html")

        if user.email_address == email:
            user.update(is_confirmed=True, confirmed_on=datetime.now())
            return render_template("success_confirm.html")
