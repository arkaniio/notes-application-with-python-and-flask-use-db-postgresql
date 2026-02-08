from app import db
from datetime import datetime

class Notes(db.Model):

    #define the name of the table from db
    __tablename__ = "notes"