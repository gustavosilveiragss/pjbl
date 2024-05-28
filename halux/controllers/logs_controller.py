from flask import Blueprint, request, jsonify
from utils import utils
from models.db import db
from models.mqtt_logs import MqttLogs

logs = Blueprint(
    name="logs",
    import_name=__name__,
    root_path="./",
    static_folder="./static/",
    template_folder="./templates/",
)

@logs.route("/")
def logs_list():
    utils.data["active_page"] = "logs"
    mqtt_logs = db.session.query(MqttLogs).order_by(MqttLogs.created_at).all()
    utils.data["logs"] = reversed(mqtt_logs)
    return utils.render_template_if_authenticated("logs.jinja")
