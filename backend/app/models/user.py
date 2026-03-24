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

    #make the relationship with db note
    notes = db.relationship("Note", back_populates="users", lazy=True)

    likes = db.relationship("Like", back_populates="users", lazy=True)

    #hashing password
    def set_password(self, password_user):
        self.password = bcrypt.generate_password_hash(password_user).decode("utf-8")
        
    #checking and compare the hashing password to the new password from user
    def check_password(self, password_hash):
        return bcrypt.check_password_hash(self.password, password_hash)
    
    #return a format into a json format when wants to convert it into json
    def to_Json(self, include_note: bool = True, include_like: bool = True):
        data = {
            "username": self.username,
            "email": self.email,
            "profile_image": self.profile_image,
            "thumbnail_image": self.thumbnail_img,
            "created_at": self.created_at.isoformat()
        }
        #validate the user note and if the like was included
        if include_note:
            data["note"] = [note.to_Json(include_user=False) for note in self.notes]
        if include_like:
            data["like"] = [like.to_Json(include_user=False, include_note=True) for like in self.likes]

        return data
