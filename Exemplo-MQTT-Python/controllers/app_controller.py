from flask import Flask, request, jsonify, render_template
from flask_mqtt import Mqtt
from models import db, instance, Read
from utils.create_db import create_db
from datetime import datetime
from controllers.iot_controller import iot
from models.mqtt import mqtt_client, topic_subscribe


def create_app() -> Flask:
    app = Flask(
        __name__,
        root_path="./",
        static_folder="./static/",
        template_folder="./templates/",
    )

    app.register_blueprint(iot, url_prefix="/iot")

    app.config["MQTT_BROKER_URL"] = "broker.hivemq.com"
    app.config["MQTT_BROKER_PORT"] = 1883
    app.config["MQTT_USERNAME"] = (
        ""  # Set this item when you need to verify username and password
    )
    app.config["MQTT_PASSWORD"] = (
        ""  # Set this item when you need to verify username and password
    )
    app.config["MQTT_KEEPALIVE"] = 5  # Set KeepAlive time in seconds
    app.config["MQTT_TLS_ENABLED"] = False  # If your broker supports TLS, set it True
    app.config["SQLALCHEMY_DATABASE_URI"] = instance

    mqtt_client.init_app(app)
    db.init_app(app)

    @app.route("/")
    def index():
        return render_template("app.html")

    @mqtt_client.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully")
            for topic in topic_subscribe:
                mqtt_client.subscribe(topic)  # subscribe topic
        else:
            print("Bad connection. Code:", rc)

    @mqtt_client.on_message()
    def handle_mqtt_message(client, userdata, message):
        data = dict(topic=message.topic, payload=message.payload.decode())
        with app.app_context():
            luminosidade = Read(
                date_time=datetime.now(), message=message.payload.decode()
            )
            db.session.add(luminosidade)
            db.session.commit()

        print(
            "Received message on topic: {topic} with payload: {payload}".format(**data)
        )

    @app.route("/publish", methods=["GET", "POST"])
    def publish_message():
        request_data = request.get_json()
        print(request_data)
        publish_result = mqtt_client.publish(
            request_data["topic"], request_data["message"]
        )
        return jsonify(publish_result)

    return app
