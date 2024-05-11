from flask import Flask, request, jsonify, render_template
import utils.consts as consts
from datetime import datetime
from controllers.iot_controller import iot
from models.db import instance, db
from models.mqtt import mqtt_client, topics_subscribe, handleMessage
from models.fake_db import *


def create_app() -> Flask:
    app = Flask(
        __name__,
        root_path="./",
        static_folder="./static/",
        template_folder="./templates/",
    )

    app.register_blueprint(iot, url_prefix="/iot")

    app.config["MQTT_BROKER_URL"] = consts.BROKER_URL
    app.config["MQTT_BROKER_PORT"] = consts.BROKER_PORT
    app.config["MQTT_KEEPALIVE"] = consts.BROKER_KEEPALIVE
    app.config["MQTT_TLS_ENABLED"] = consts.BROKER_TLS_ENABLED
    app.config["SQLALCHEMY_DATABASE_URI"] = instance

    mqtt_client.init_app(app)
    db.init_app(app)

    data_maestro = dict(active_page="dashboard")

    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
            for topic in topics_subscribe:
                mqtt_client.subscribe(topic)
        else:
            print("Bad connection. Code:", rc)

    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        path = message.topic.split("/")

        topic = path[0]
        subtopic = path[1]
        topicID = path[2]

        if subtopic == consts.REQUEST:
            operation = path[3]
        else:
            operation = consts.RESPONSE

        payload = message.payload.decode("utf-8")

        log = dict(
            mqtt_log_id=len(mqtt_logs) + 1,
            created_at=datetime.now(),
            topic=topic,
            subtopic=subtopic,
            device_id=topicID,
            operation=operation,
            payload=payload,
        )

        mqtt_logs.append(log)

        print(
            f"Time: {datetime.now()} | Topic: {topic} | Subtopic: {subtopic} | Topic ID: {topicID} | Operation: {operation} | Payload: {payload}"
        )

        if subtopic == consts.REQUEST:
            handleMessage(client, topic, topicID, operation, payload)

    @app.route("/")
    def index():
        return render_template("app.jinja", data=data_maestro)

    @app.route("/publish", methods=["POST"])
    def publish_message():
        request_data = request.get_json()
        print(request_data)

        result, _ = mqtt_client.publish(request_data["topic"], request_data["message"])

        return jsonify(result)

    @app.route("/logs")
    def logs():
        return render_template("logs.jinja", data=data_maestro)

    return app
