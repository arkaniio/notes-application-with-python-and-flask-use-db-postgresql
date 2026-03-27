from app import db
from datetime import datetime
import uuid

class Like(db.Model):

    #define the name of the table db
    __tablename__ = "likes"

    #define the field of the database likes
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    note_id = db.Column(db.String(36), db.ForeignKey("notes.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    #define the relationship between user and like and note and like
    users = db.relationship("User", back_populates="likes")

    notes = db.relationship("Note", back_populates="likes")

    def to_Json(self, include_user: bool = False, include_note: bool = False):

        data = {
            "id": self.id,
            "user_id": self.user_id,
            "note_id": self.note_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

        if include_user and self.users:
            data["user"] = {
                "id": self.users.id,
                "username": self.users.username,
                "email": self.users.email
            }
        if include_note and self.notes:
            data["note"] = self.notes.to_Json(include_user=True, include_like=False)
        
        return data

