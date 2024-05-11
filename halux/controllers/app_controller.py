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
                mqtt_client.subscribe(topic, 1)
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

        if subtopic == consts.REQUEST:
            handleMessage(client, topic, topicID, operation, payload)

    @app.route("/")
    def index():
        data_maestro["active_page"] = "dashboard"
        return render_template("app.jinja", data=data_maestro)

    @app.route("/publish", methods=["POST"])
    def publish_message():
        request_data = request.get_json()
        result, _ = mqtt_client.publish(request_data["topic"], request_data["message"])
        return jsonify(result)

    @app.route("/logs")
    def logs():
        data_maestro["active_page"] = "logs"
        data_maestro["logs"] = reversed(mqtt_logs)
        return render_template("logs.jinja", data=data_maestro)

    @app.route("/devices")
    def devices_route():
        data_maestro["active_page"] = "devices"
        data_maestro["devices"] = device
        return render_template("devices.jinja", data=data_maestro)

    @app.route("/devices/<int:device_id>")
    def device_route(device_id):
        data_maestro["active_page"] = "devices"

        # Proper query with the joins will be implmeented once the database gets created
        d = None
        for d_db in device:
            if d_db["device_id"] == device_id:
                d = d_db
                break
        if d is None:
            data_maestro["devices"] = device
            return render_template("devices.jinja", data=data_maestro)

        data_maestro["device"] = d
        data_maestro["sensors"] = []
        data_maestro["actuators"] = []

        for d_s in device_sensor:
            if d_s["device_id"] == device_id:
                sensor = dict(sensor_id=d_s["sensor_model_id"])
                for s in sensor_model:
                    if s["sensor_model_id"] == d_s["sensor_model_id"]:
                        sensor["name"] = s["name"]
                        break
                data_maestro["sensors"].append(sensor)
        for d_a in device_actuator:
            if d_a["device_id"] == device_id:
                actuator = dict(actuator_id=d_a["actuator_model_id"])
                for a in actuator_model:
                    if a["actuator_model_id"] == d_a["actuator_model_id"]:
                        actuator["name"] = a["name"]
                        break
                data_maestro["actuators"].append(actuator)

        return render_template("edit_device.jinja", data=data_maestro)

    @app.route("/edit_device", methods=["PUT"])
    def edit_device():
        request_data = request.get_json()
        device_id = request_data["device_id"]
        device_name = request_data["name"]

        d = None
        for d_db in device:
            if d_db["device_id"] == device_id:
                d = d_db
                break
        if d is None:
            return jsonify({"status": "Device not found"}), 400

        d["device_name"] = device_name

        return jsonify({"status": "OK"})

    @app.route("/delete_device", methods=["DELETE"])
    def delete_device():
        request_data = request.get_json()
        device_id = request_data["device_id"]

        d = None
        for d_db in device:
            if d_db["device_id"] == device_id:
                d = d_db
                break
        if d is None:
            return jsonify({"status": "Device not found"}), 400

        device.remove(d)

        return jsonify({"status": "OK"})

    @app.route("/devices/new")
    def new_device():
        data_maestro["active_page"] = "devices"
        data_maestro["sensors"] = sensor_model
        data_maestro["actuators"] = actuator_model
        return render_template("new_device.jinja", data=data_maestro)

    @app.route("/new_device", methods=["POST"])
    def create_device():
        request_data = request.get_json()
        device_name = request_data["name"]

        device_id = len(device) + 1
        device.append(
            dict(device_id=device_id, device_name=device_name, created_at=datetime.now())
        )

        for s in sensor_model:
            device_sensor.append(
                dict(
                    device_id=device_id,
                    sensor_model_id=s["sensor_model_id"],
                )
            )

        for a in actuator_model:
            device_actuator.append(
                dict(
                    device_id=device_id,
                    actuator_model_id=a["actuator_model_id"],
                )
            )

        return jsonify({"status": "OK"})

    return app
