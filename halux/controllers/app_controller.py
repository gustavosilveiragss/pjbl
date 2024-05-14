from flask import Flask, request, jsonify, render_template, redirect, make_response
import utils.consts as consts
import utils.utils as utils
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

    # app.config["MQTT_BROKER_URL"] = consts.BROKER_URL
    # app.config["MQTT_BROKER_PORT"] = consts.BROKER_PORT
    # app.config["MQTT_KEEPALIVE"] = consts.BROKER_KEEPALIVE
    # app.config["MQTT_TLS_ENABLED"] = consts.BROKER_TLS_ENABLED
    app.config["SQLALCHEMY_DATABASE_URI"] = instance

    # mqtt_client.init_app(app)
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
                        utils.data["temperature"] = d_s["value"]
                    case 2:
                        utils.data["humidity"] = d_s["value"]
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

    @app.route("/publish", methods=["POST"])
    def publish_message():
        request_data = request.get_json()
        result, _ = mqtt_client.publish(request_data["topic"], request_data["message"])
        return jsonify(result)

    @app.route("/logs")
    def logs():
        utils.data["active_page"] = "logs"
        utils.data["logs"] = reversed(mqtt_logs)
        return utils.render_template_if_authenticated("logs.jinja")

    @app.route("/devices")
    def devices_route():
        utils.data["active_page"] = "devices"
        utils.data["devices"] = device
        return utils.render_template_if_authenticated("devices.jinja")

    @app.route("/devices/<int:device_id>")
    def device_route(device_id):
        utils.data["active_page"] = "devices"

        # Proper query with the joins will be implmeented once the database gets created
        d = None
        for d_db in device:
            if d_db["device_id"] == device_id:
                d = d_db
                break
        if d is None:
            return redirect("/devices")

        utils.data["device"] = d
        utils.data["sensors"] = []
        utils.data["actuators"] = []

        for d_s in device_sensor:
            if d_s["device_id"] == device_id:
                sensor = dict(sensor_id=d_s["sensor_model_id"])
                for s in sensor_model:
                    if s["sensor_model_id"] == d_s["sensor_model_id"]:
                        sensor["name"] = s["name"]
                        break
                utils.data["sensors"].append(sensor)
        for d_a in device_actuator:
            if d_a["device_id"] == device_id:
                actuator = dict(actuator_id=d_a["actuator_model_id"])
                for a in actuator_model:
                    if a["actuator_model_id"] == d_a["actuator_model_id"]:
                        actuator["name"] = a["name"]
                        break
                utils.data["actuators"].append(actuator)

        return utils.render_template_if_authenticated("edit_device.jinja")

    @app.route("/edit_device", methods=["PUT"])
    def edit_device():
        request_data = request.get_json()
        device_id = request_data["device_id"]
        if device_id == 1:
            return jsonify({"status": "Cannot edit the central Halux device"}), 400

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
        if device_id == 1:
            return jsonify({"status": "Cannot delete the central Halux device"}), 400

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
        utils.data["active_page"] = "devices"
        utils.data["sensors"] = sensor_model
        utils.data["actuators"] = actuator_model
        return utils.render_template_if_authenticated("new_device.jinja")

    @app.route("/new_device", methods=["POST"])
    def create_device():
        request_data = request.get_json()
        device_name = request_data["name"]

        device_id = len(device) + 1
        device.append(
            dict(
                device_id=device_id, device_name=device_name, created_at=datetime.now()
            )
        )

        for s in sensor_model:
            device_sensor.append(
                dict(
                    device_id=device_id,
                    sensor_model_id=s["sensor_model_id"],
                    updated_at=datetime.now(),
                    value=None,
                )
            )

        for a in actuator_model:
            device_actuator.append(
                dict(
                    device_id=device_id,
                    actuator_model_id=a["actuator_model_id"],
                    updated_at=datetime.now(),
                    value=None,
                )
            )

        return jsonify({"status": "OK"})

    @app.route("/users")
    def users_route():
        return utils.render_template_if_authenticated("users.jinja", users=user)

    @app.route("/users/new")
    def user_device():
        utils.data["active_page"] = "users"
        return utils.render_template_if_authenticated("new_user.jinja")

    @app.route("/new_user", methods=["POST"])
    def create_user():
        username = request.json["username"]
        password = request.json["password"]

        user_id = len(user) + 1
        user.append(
            dict(
                user_id=user_id,
                username=username,
                password=password,
                created_at=datetime.now(),
            )
        )

        return jsonify({"status": "OK"})

    @app.route("/users/<int:user_id>")
    def edit_user_route(user_id):
        utils.data["active_page"] = "users"

        u = None
        for u_db in user:
            if u_db["user_id"] == user_id:
                u = u_db
                break
        if u is None:
            return utils.render_template_if_authenticated("users.jinja")

        return utils.render_template_if_authenticated("edit_user.jinja", user=u)

    @app.route("/edit_user", methods=["PUT"])
    def edit_user():
        user_id = request.json["user_id"]

        username = request.json["username"]
        password = request.json["password"]

        u = None
        for u_db in user:
            if u_db["user_id"] == user_id:
                u = u_db
                break
        if u is None:
            return jsonify({"status": "User not found"}), 400

        u["username"] = username
        u["password"] = password

        return jsonify({"status": "OK"})

    @app.route("/delete_user", methods=["DELETE"])
    def delete_user():
        user_id = request.json["user_id"]
        if user_id == 1:
            return jsonify({"status": "Cannot delete the admin user"}), 400

        u = None
        for u_db in user:
            if u_db["user_id"] == user_id:
                u = u_db
                break
        if u is None:
            return jsonify({"status": "User not found"}), 400

        user.remove(u)
        if user_id == request.cookies["user_id"]:
            request.cookies.pop("user_id")

        return jsonify({"status": "OK"})

    return app
