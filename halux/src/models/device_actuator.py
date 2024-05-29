from datetime import datetime
from models.db import Base, db


class DeviceActuator(Base):
    __tablename__ = "device_actuator"

    device_actuator_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    device_id = db.Column(db.Integer, db.ForeignKey("device.device_id"), nullable=False)
    actuator_model_id = db.Column(
        db.Integer, db.ForeignKey("actuator_model.actuator_model_id"), nullable=False
    )
    value = db.Column(db.String(255), nullable=False)

    device = db.relationship("Device", back_populates="device_actuators")
    actuator_model = db.relationship("ActuatorModel", back_populates="device_actuators")
