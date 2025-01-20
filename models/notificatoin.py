from extension import db
from models.user import UserModel
from models.base import BaseModel

class NotificationModel(BaseModel):
    __tablename__= "notification"
    user_id = db.Column(db.String(120), db.ForeignKey("user.id"))
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    image_url = db.Column(db.TEXT, nullable=True)
    route = db.Column(db.String(40), default="/homeScreen")
    user =  db.relationship("UserModel", back_populates="notifications")

