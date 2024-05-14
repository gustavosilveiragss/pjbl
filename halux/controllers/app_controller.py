from flask import Flask, request, jsonify, render_template, redirect, make_response
import utils.consts as consts
import utils.utils as utils
from datetime import datetime
from controllers.iot_controller import iot
from models.db import instance, db
from models.mqtt import mqtt_client, topics_subscribe, handleMessage
from models.fake_db import *
from controllers.users_controller import users
from controllers.devices_controller import devices


def create_app() -> Flask:
    app = Flask(
        __name__,
        root_path="./",
        static_folder="./static/",
        template_folder="./templates/",
    )

    app.register_blueprint(iot, url_prefix="/iot")
    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(devices, url_prefix="/devices")

    app.config["MQTT_BROKER_URL"] = consts.BROKER_URL
    app.config["MQTT_BROKER_PORT"] = consts.BROKER_PORT
    app.config["MQTT_KEEPALIVE"] = consts.BROKER_KEEPALIVE
    app.config["MQTT_TLS_ENABLED"] = consts.BROKER_TLS_ENABLED
    app.config["SQLALCHEMY_DATABASE_URI"] = instance

    mqtt_client.init_app(app)
    db.init_app(app)

    @app.route("/")
    def index():
        if utils.is_authenticated():
            return redirect("/dashboard")
        else:
            return redirect("/login")

    @app.route("/login")
    def login():
        utils.data["active_page"] = ""
        return render_template("login.jinja", data=utils.data, cookies=request.cookies)

    @app.route("/authenticate", methods=["POST"])
    def authenticate():
        username = request.json["username"]
        password = request.json["password"]

        u = None
        for u_db in user:
            if u_db["username"] == username and u_db["password"] == password:
                u = u_db
                break
        if u is None:
            return jsonify({"status": "User not found"}), 400

        utils.data["user_id"] = u_db["user_id"]
        resp = make_response(jsonify(status="ok"))
        resp.set_cookie("user_id", str(u_db["user_id"]))
        return resp

    @app.route("/dashboard")
    def dashboard_default():
        utils.data["active_page"] = "dashboard"

        # Redirect to the first device that is not the central Halux device, if it exists
        for d in device:
            if d["device_id"] != 1:
                return redirect("/dashboard/" + str(d["device_id"]))

        return redirect("/devices")

    @app.route("/dashboard/<int:device_id>")
    def dashboard(device_id):
        utils.data["active_page"] = "dashboard"

        d = None
        for d_db in device:
            if d_db["device_id"] == device_id:
                d = d_db
                break
        if d is None or d["device_id"] == 1:
            return redirect("/devices")

        utils.data["device"] = d

        utils.data["devices"] = [d]
        for d_db in device:
            if d_db["device_id"] != device_id and d_db["device_id"] != 1:
                utils.data["devices"].append(d_db)

        for d_s in device_sensor:
            if d_s["device_id"] == device_id:
                match d_s["sensor_model_id"]:
                    case 1:
                        utils.data["temperature"] = f"{(d_s['value'] or 0.0):.2f}"
                    case 2:
                        utils.data["humidity"] = f"{(d_s['value'] or 0.0):.2f}"
                    case 3:
                        utils.data["open"] = d_s["value"]

        for d_a in device_actuator:
            if d_a["device_id"] == device_id:
                if d_a["actuator_model_id"] == 2:
                    utils.data["frequency"] = d_a["value"]

        return utils.render_template_if_authenticated("dashboard.jinja")

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

        print(f"Received message: {topic}/{subtopic}/{topicID}/{operation} - {payload}")

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

    @app.route("/publish_mqtt", methods=["POST"])
    def publish_message():
        request_data = request.get_json()
        topic = request_data["topic"]
        result, _ = mqtt_client.publish(topic, request_data["payload"], 1)

        jsonRes = jsonify(result)

        if jsonRes.status == "ERROR":
            return jsonRes

        topic = topic[:-1] + "R"
        print(topic)

        result, _ = mqtt_client.publish(topic, request_data["payload"], 1)
        return jsonify(result)

    @app.route("/logs")
    def logs():
        utils.data["active_page"] = "logs"
        utils.data["logs"] = reversed(mqtt_logs)
        return utils.render_template_if_authenticated("logs.jinja")

    return app
