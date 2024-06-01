from flask import Flask, request, jsonify, render_template, redirect, make_response
from models.mqtt_logs import MqttLogs
from models.user import User
from models.device import Device
import utils.consts as consts
import utils.utils as utils
from datetime import datetime
from models.db import instance, db
from models.mqtt import mqtt_client, topics_subscribe, handle_message
from controllers.users_controller import users
from controllers.devices_controller import devices
from controllers.logs_controller import logs


def create_app() -> Flask:
    app = Flask(
        __name__,
        root_path="./",
        static_folder="./static/",
        template_folder="./templates/",
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = instance
    app.config["TESTING"] = False
    app.config["SECRET_KEY"] = "PJBL"
    db.init_app(app)

    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(devices, url_prefix="/devices")
    app.register_blueprint(logs, url_prefix="/logs")

    app.config["MQTT_BROKER_URL"] = consts.BROKER_URL
    app.config["MQTT_BROKER_PORT"] = consts.BROKER_PORT
    app.config["MQTT_KEEPALIVE"] = consts.BROKER_KEEPALIVE
    app.config["MQTT_TLS_ENABLED"] = consts.BROKER_TLS_ENABLED

    mqtt_client.init_app(app)

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

    @app.route("/logout")
    def logout():
        resp = redirect("/login")
        resp.delete_cookie("user_id")
        return resp

    @app.route("/authenticate", methods=["POST"])
    def authenticate():
        username = request.json["username"]
        password = request.json["password"]

        u = (
            db.session.query(User)
            .filter(User.username == username, User.password == password)
            .first()
        )
        if u is None:
            return jsonify({"status": "User not found"}), 400

        resp = make_response(jsonify(status="ok"))
        resp.set_cookie("user_id", str(u.user_id))
        return resp

    @app.route("/dashboard")
    def dashboard_default():
        utils.data["active_page"] = "dashboard"

        # Redirect to the first device that is not the central Halux device, if it exists
        device = db.session.query(Device).filter(Device.device_id != 1).first()
        if device is not None:
            return redirect(f"/dashboard/{device.device_id}")

        return redirect("/devices")

    @app.route("/dashboard/<int:device_id>")
    def dashboard(device_id):
        utils.data["active_page"] = "dashboard"

        d = db.session.query(Device).filter(Device.device_id == device_id).first()
        if d is None or d.device_id == 1:
            return redirect("/devices")

        utils.data["device"] = d

        utils.data["devices"] = [d]
        ds = (
            db.session.query(Device)
            .filter(Device.device_id != device_id, Device.device_id != 1)
            .all()
        )
        if ds is not None:
            utils.data["devices"] += ds

        for d_s in d.device_sensors:
            match d_s.sensor_model_id:
                case 1:
                    utils.data["temperature"] = f"{(float(d_s.value) or 0.0):.2f}"
                case 2:
                    utils.data["humidity"] = f"{(float(d_s.value) or 0.0):.2f}"
                case 3:
                    utils.data["open"] = float(d_s.value)

        for d_a in d.device_actuators:
            if d_a.actuator_model_id == 2:
                utils.data["frequency"] = d_a.value

        user_id = utils.get_user_id()
        role = db.session.query(User.role).filter(User.user_id == user_id).first()
        can_send_commands = role[0] != "statistics"

        return utils.render_template_if_authenticated(
            "dashboard.jinja", can_send_commands=can_send_commands
        )

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

        log = MqttLogs(
            created_at=datetime.now(),
            topic=topic,
            subtopic=subtopic,
            device_id=topicID,
            operation=operation,
            payload=payload,
        )

        with app.app_context():
            db.session.add(log)
            db.session.commit()

        if subtopic == consts.REQUEST:
            handle_message(topic, topicID, operation, payload, app)

    @app.route("/publish_mqtt", methods=["POST"])
    def publish_message():
        request_data = request.get_json()
        topic = request_data["topic"]
        result, _ = mqtt_client.publish(topic, request_data["payload"], 1)

        jsonRes = jsonify(result)

        if jsonRes.status == "ERROR":
            return jsonRes

        topic = topic[:-1] + "R"

        result, _ = mqtt_client.publish(topic, request_data["payload"], 1)
        return jsonify(result)

    return app
