from datetime import datetime
from models.db import Base, db


class MqttLogs(Base):
    __tablename__ = "mqtt_logs"

    mqtt_log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    topic = db.Column(db.String(255), nullable=False)
    subtopic = db.Column(db.String(255), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey("device.device_id"), nullable=False)
    operation = db.Column(db.String(255), nullable=False)
    payload = db.Column(db.String(255), nullable=False)

    device = db.relationship("Device", back_populates="mqtt_logs")
