from datetime import datetime
from models.db import Base, db


class DeviceSensor(Base):
    __tablename__ = "device_sensor"

    device_sensor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    device_id = db.Column(db.Integer, db.ForeignKey("device.device_id"), nullable=False)
    sensor_model_id = db.Column(
        db.Integer, db.ForeignKey("sensor_model.sensor_model_id"), nullable=False
    )
    value = db.Column(db.String(255), nullable=False)

    device = db.relationship("Device", back_populates="device_sensors")
    sensor_model = db.relationship("SensorModel", back_populates="device_sensors")
