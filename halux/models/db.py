from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

Base = declarative_base()

instance = "mysql+pymysql://halux:halux@localhost:3306/pjbl"

def create_db(app: Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()