from models import db
from datetime import datetime

class Read(db.Model):
    __tablename__ = "reads"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    date_time = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    message = db.Column(db.String(100), nullable=False)