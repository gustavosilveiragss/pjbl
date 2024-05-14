from flask import Blueprint, request, jsonify
from utils import utils
from datetime import datetime
from models.fake_db import *

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
    utils.data["devices"] = device
    return utils.render_template_if_admin("devices.jinja")


@devices.route("/<int:device_id>")
def device_route(device_id):
    utils.data["active_page"] = "devices"

    # Proper query with the joins will be implmeented once the database gets created
    d = None
    for d_db in device:
        if d_db["device_id"] == device_id:
            d = d_db
            break
    if d is None:
        return redirect("/")

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

    return utils.render_template_if_admin("edit_device.jinja")


@devices.route("/edit_device", methods=["PUT"])
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


@devices.route("/delete_device", methods=["DELETE"])
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


@devices.route("/new")
def new_device():
    utils.data["active_page"] = "devices"
    utils.data["sensors"] = sensor_model
    utils.data["actuators"] = actuator_model
    return utils.render_template_if_admin("new_device.jinja")


@devices.route("/new_device", methods=["POST"])
def create_device():
    request_data = request.get_json()
    device_name = request_data["name"]

    device_id = device[-1]["device_id"] + 1
    device.append(
        dict(device_id=device_id, device_name=device_name, created_at=datetime.now())
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
