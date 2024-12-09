from db import db
import uuid
from datetime import datetime


class AuthToken(db.Model):
    auth_token = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.user_id'), nullable=False)
    expiration = db.Column(db.DateTime, default=datetime.utcnow)
