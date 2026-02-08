from app import db, bcrypt
from datetime import datetime
import uuid

class User(db.Model):

    #define the table name from db
    __tablename__ = "users"

    #initiation the fields of the database
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(30), nullable=True, unique=False)
    email = db.Column(db.String(30), nullable=True, unique=True)
    password = db.Column(db.String(255), nullable=True)
    profile_image = db.Column(db.String(255))
    thumbnail_img = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    #hashing password
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    #checking and compare the hashing password to the new password from user
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
