from flask import Blueprint, request, jsonify, redirect
from models.mqtt_logs import MqttLogs
from models.device import Device
from models.device_sensor import DeviceSensor
from models.device_actuator import DeviceActuator
from models.sensor_model import SensorModel
from models.actuator_model import ActuatorModel
from utils import utils
from datetime import datetime
from models.db import db
from sqlalchemy import asc

devices = Blueprint(
    name="devices",
    import_name=__name__,
    root_path="./",
    static_folder="./static/",
    template_folder="./templates/",
)


@devices.route("/")
def devices_route():
    utils.data["active_page"] = "devices"
    devices = db.session.query(Device).order_by(asc(Device.created_at)).all()
    utils.data["devices"] = devices
    return utils.render_template_if_admin("devices.jinja")


@devices.route("/<int:device_id>")
def device_route(device_id):
    utils.data["active_page"] = "devices"

    d = db.session.query(Device).filter(Device.device_id == device_id).first()
    if d is None:
        return redirect("/")

    utils.data["device"] = d
    utils.data["sensors"] = (
        db.session.query(
            DeviceSensor.device_sensor_id, SensorModel.sensor_model_id, SensorModel.name
        )
        .filter(DeviceSensor.device_id == device_id)
        .join(SensorModel, SensorModel.sensor_model_id == DeviceSensor.sensor_model_id)
        .all()
    )
    utils.data["actuators"] = (
        db.session.query(
            DeviceActuator.device_actuator_id,
            ActuatorModel.actuator_model_id,
            ActuatorModel.name,
        )
        .filter(DeviceActuator.device_id == device_id)
        .join(
            ActuatorModel,
            ActuatorModel.actuator_model_id == DeviceActuator.actuator_model_id,
        )
        .all()
    )

    return utils.render_template_if_admin("edit_device.jinja")


@devices.route("/edit_device", methods=["PUT"])
def edit_device():
    request_data = request.get_json()
    device_id = request_data["device_id"]
    if device_id == 1:
        return jsonify({"status": "Cannot edit the central Halux device"}), 400

    device_name = request_data["name"]

    d = db.session.query(Device).filter(Device.device_id == device_id).first()
    if d is None:
        return jsonify({"status": "Device not found"}), 400

    d.device_name = device_name
    db.session.commit()

    return jsonify({"status": "OK"})


@devices.route("/delete_device", methods=["DELETE"])
def delete_device():
    request_data = request.get_json()
    device_id = request_data["device_id"]
    if device_id == 1:
        return jsonify({"status": "Cannot delete the central Halux device"}), 400

    db.session.query(DeviceSensor).filter(DeviceSensor.device_id == device_id).delete()
    db.session.query(DeviceActuator).filter(DeviceActuator.device_id == device_id).delete()
    db.session.query(MqttLogs).filter(MqttLogs.device_id == device_id).delete()
    db.session.query(Device).filter(Device.device_id == device_id).delete()
    db.session.commit()

    return jsonify({"status": "OK"})


@devices.route("/new")
def new_device():
    utils.data["active_page"] = "devices"
    utils.data["sensors"] = db.session.query(SensorModel).all()
    utils.data["actuators"] = db.session.query(ActuatorModel).all()
    return utils.render_template_if_admin("new_device.jinja")


@devices.route("/new_device", methods=["POST"])
def create_device():
    request_data = request.get_json()
    device_name = request_data["name"]

    d = Device(
        device_name=device_name,
        created_at=datetime.now(),
        user_id=utils.get_user_id(),
        password="000",
        permission_state=0
    )

    db.session.add(d)
    db.session.flush()

    device_id = d.device_id

    sensor_model = db.session.query(SensorModel).all()

    for s in sensor_model:
        db.session.add(
            DeviceSensor(
                device_id=device_id,
                sensor_model_id=s.sensor_model_id,
                updated_at=datetime.now(),
                value=0,
            )
        )

    actuator_model = db.session.query(ActuatorModel).all()

    for a in actuator_model:
        db.session.add(
            DeviceActuator(
                device_id=device_id,
                actuator_model_id=a.actuator_model_id,
                updated_at=datetime.now(),
                value=0,
            )
        )

    db.session.commit()

    return jsonify({"status": "OK"})
