from datetime import datetime
from models.db import Base, db

class SensorModel(Base):
    __tablename__ = "sensor_model"

    sensor_model_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(255), nullable=False)

    device_sensors = db.relationship("DeviceSensor", back_populates="sensor_model")