from app import db
from datetime import datetime
import uuid
from app import bcrypt
from sqlalchemy import Enum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func
from app.models.likes import Like

class Note(db.Model):

    #define the name of the table from db
    __tablename__ = "notes"

    #define the field of the database
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(Enum("private", "public", "protected", name="notes_status"), default="public", nullable=False)
    password = db.Column(db.String(255), nullable=True)
    password_hint = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    #make the relationship from users to notes and with like
    users = db.relationship("User", back_populates="notes")

    likes = db.relationship("Like", back_populates="notes")

    #make the func that count the len of likes
    @hybrid_property
    def like_count(self):
        return len(self.likes)
    
    @like_count.expression
    def like_count(lc):
        return (
            select([func.count(Like.id)]).where(Like.note_id == lc.id).label("like_count")
        )

    #encode password
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
    
    #checking the encode of the password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    #encoding into a json type
    def to_Json(self, include_user: bool = True, include_like: bool = True):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "slug": self.slug,
            "content": self.content,
            "status": self.status,
            "password_hint": self.password_hint,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "like_count": self.like_count
        }
        #validate the user if the note have a same user
        if include_user and self.users:
            data["user"] = self.users.to_Json(include_note=False, include_like=True)
        if include_like:
            data["like"] = [like.to_Json(include_note=False, include_user=True) for like in self.likes]

        return data

