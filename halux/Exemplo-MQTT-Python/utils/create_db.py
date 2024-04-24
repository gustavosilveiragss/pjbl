from models import *
from flask import Flask

def create_db(app:Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()