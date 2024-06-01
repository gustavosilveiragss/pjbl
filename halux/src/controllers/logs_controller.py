from datetime import datetime, timedelta
from flask import Blueprint, request
from models.device import Device
from utils import utils
import utils.consts as consts
from models.db import db
from models.mqtt_logs import MqttLogs
from models.user import User
from sqlalchemy import desc

logs = Blueprint(
    name="logs",
    import_name=__name__,
    root_path="./",
    static_folder="./static/",
    template_folder="./templates/",
)

valid_topics = [
    consts.TOP_PERMISSION_STATE,
    consts.TOP_IR_STATE,
    consts.TOP_PASSWORD,
    consts.TOP_FREQUENCY,
    consts.TOP_TEMPERATURE,
    consts.TOP_HUMIDITY,
    consts.TOP_DEVICE,
    consts.TOP_USER,
]

valid_subtopics = [consts.REQUEST, consts.RESPONSE, consts.CRUD]

valid_operations = [consts.READ, consts.WRITE, consts.DELETE]


@logs.route("/")
def logs_list():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    topic = request.args.get("topic")
    subtopic = request.args.get("subtopic")
    device_id = request.args.get("device_id")
    operation = request.args.get("operation")

    query = db.session.query(MqttLogs).order_by(desc(MqttLogs.created_at))

    if start_date:
        query = query.filter(MqttLogs.created_at >= start_date)

    if end_date:
        # Up to 23:59:59
        end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(
            days=1, seconds=-1
        )
        query = query.filter(MqttLogs.created_at <= end_date)

    if topic and topic in valid_topics:
        query = query.filter(MqttLogs.topic == topic)

    if subtopic and subtopic in valid_subtopics:
        query = query.filter(MqttLogs.subtopic == subtopic)

    if device_id:
        query = query.filter(MqttLogs.device_id == device_id)

    if operation and operation in valid_operations:
        query = query.filter(MqttLogs.operation == operation)

    role = (
        db.session.query(User.role).filter(User.user_id == utils.get_user_id()).first()
    )
    if role[0] == "statistics":
        query = query.filter(MqttLogs.subtopic != consts.CRUD)

    mqtt_logs = query.all()

    utils.data["active_page"] = "logs"
    utils.data["logs"] = mqtt_logs
    utils.data["topics"] = valid_topics
    utils.data["subtopics"] = valid_subtopics
    utils.data["operations"] = valid_operations
    utils.data["devices"] = db.session.query(Device.device_id, Device.device_name).all()

    return utils.render_template_if_authenticated("logs.jinja")
