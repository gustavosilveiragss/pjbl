from datetime import datetime
from models.db import Base, db

class ActuatorModel(Base):
    __tablename__ = "actuator_model"

    actuator_model_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(255), nullable=False)

    device_actuators = db.relationship("DeviceActuator", back_populates="actuator_model")