from datetime import datetime
from models.db import Base, db


class Device(Base):
    __tablename__ = "device"

    device_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    device_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(3), nullable=False)
    permission_state = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", back_populates="devices", lazy=True)
    device_actuators = db.relationship("DeviceActuator", back_populates="device")
    device_sensors = db.relationship("DeviceSensor", back_populates="device")
    mqtt_logs = db.relationship("MqttLogs", back_populates="device")
