from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import utils.consts as consts

db = SQLAlchemy()
instance = "sqlite:///luminosidade"

def createDB(app):
    with app.app_context():
        db.init_app(app)

        # load from dump file
        with open("../dump.sql", "r") as file:
            db.session.execute(file.read())
            db.session.commit()

        db.create_all()

def readDB(key):
    print(key)
    print(db.session.query("IR_STATE"))
    return db.session.query(key).first()
    