import utils.consts as consts
from flask_mqtt import Mqtt
from models.db import db
from models.device import Device
from models.device_sensor import DeviceSensor
from models.device_actuator import DeviceActuator

mqtt_client = Mqtt()

topics_subscribe = [
    consts.TOP_PERMISSION_STATE + "/#",
    consts.TOP_IR_STATE + "/#",
    consts.TOP_PASSWORD + "/#",
    consts.TOP_FREQUENCY + "/#",
    consts.TOP_TEMPERATURE + "/#",
    consts.TOP_HUMIDITY + "/#",
]


def returnError(msg):
    return '{"status": "ERROR", "message": "' + msg + '"}'


def emitRes(topic, payload, id):
    mqtt_client.publish(f"{topic}/{consts.RESPONSE}/{id}", payload, 1)


def handle_permission_state(payload, operation, topicID):
    device = db.session.query(Device).filter(Device.device_id == int(topicID)).first()

    if operation == consts.READ:
        res = "ALLOWED" if device.permission_state == 1 else "PROHIBITED"
        emitRes(consts.TOP_PERMISSION_STATE, res, topicID)
        return

    if payload != "0" and payload != "1":
        emitRes(
            consts.TOP_PERMISSION_STATE,
            returnError("Permission state must be either '0' or '1'"),
            topicID,
        )
        return

    device.permission_state = int(payload)
    db.session.commit()
    emitRes(consts.TOP_PERMISSION_STATE, consts.RESPONSE_OK, topicID)


def handle_ir_state(payload, operation, topicID):
    ir = (
        db.session.query(DeviceSensor)
        .filter(
            DeviceSensor.device_id == int(topicID),
            DeviceSensor.sensor_model_id == 3,
        )
        .first()
    )
    if ir is None:
        return

    if operation == consts.READ:
        res = "OPEN" if ir.value == 1 else "CLOSED"
        emitRes(consts.TOP_IR_STATE, res, topicID)
        return

    if payload != "0" and payload != "1":
        emitRes(
            consts.TOP_IR_STATE,
            returnError("IR state must be either '0' or '1'"),
            topicID,
        )
        return

    ir.value = int(payload)
    db.session.commit()
    emitRes(consts.TOP_IR_STATE, consts.RESPONSE_OK, topicID)


def handle_password(payload, operation, topicID):
    device = db.session.query(Device).filter(Device.device_id == int(topicID)).first()

    if operation == consts.READ:
        emitRes(consts.TOP_PASSWORD, device.password, topicID)
        return

    if len(payload) != 3:
        emitRes(
            consts.TOP_PASSWORD,
            returnError("Password sequence must be 3 characters long"),
            topicID,
        )
        return

    for i in payload:
        if not i.isdigit() or int(i) < 0 or int(i) > 2:
            emitRes(
                consts.TOP_PASSWORD,
                returnError(
                    "Password sequence must contain only numbers between 0 and 2"
                ),
                topicID,
            )
            return

    device.password = payload
    db.session.commit()
    emitRes(consts.TOP_PASSWORD, consts.RESPONSE_OK, topicID)


def handle_frequency(payload, operation, topicID):
    buzzer = (
        db.session.query(DeviceActuator)
        .filter(
            DeviceActuator.device_id == int(topicID),
            DeviceActuator.actuator_model_id == 2,
        )
        .first()
    )

    if buzzer is None:
        return

    if operation == consts.READ:
        emitRes(consts.TOP_FREQUENCY, buzzer.value, topicID)
        return

    if not payload.isdigit() or int(payload) < 0 or int(payload) > 10000:
        emitRes(
            consts.TOP_FREQUENCY,
            returnError("Frequency must be a number between 0 and 10000"),
            topicID,
        )
        return

    buzzer.value = int(payload)
    db.session.commit()
    emitRes(consts.TOP_FREQUENCY, consts.RESPONSE_OK, topicID)


def handle_temperature(payload, operation, topicID):
    dht = (
        db.session.query(DeviceSensor)
        .filter(
            DeviceSensor.device_id == int(topicID), DeviceSensor.sensor_model_id == 1
        )
        .first()
    )
    if dht is None:
        return

    if operation == consts.READ:
        emitRes(consts.TOP_TEMPERATURE, dht.value, topicID)
        return

    def validateTemperature():
        try:
            return float(payload) >= 0 and float(payload) <= 100
        except ValueError:
            return False

    if not validateTemperature():
        emitRes(
            consts.TOP_TEMPERATURE,
            returnError(
                "Temperature must be a number between 0.0 and 100.0, indicating the degrees celsius"
            ),
            topicID,
        )
        return

    dht.value = float(payload)
    db.session.commit()
    emitRes(consts.TOP_TEMPERATURE, consts.RESPONSE_OK, topicID)


def handle_humidity(payload, operation, topicID):
    dht = (
        db.session.query(DeviceSensor)
        .filter(
            DeviceSensor.device_id == int(topicID), DeviceSensor.sensor_model_id == 2
        )
        .first()
    )
    if dht is None:
        return

    if operation == consts.READ:
        emitRes(consts.TOP_HUMIDITY, dht.value, topicID)
        return

    def validateHumidity():
        try:
            return float(payload) >= 0 and float(payload) <= 100
        except ValueError:
            return False

    if not validateHumidity():
        emitRes(
            consts.TOP_HUMIDITY,
            returnError(
                "Humidity must be a number between 0.0 and 100.0, indicating the humidity percentage"
            ),
            topicID,
        )
        return

    dht.value = float(payload)
    db.session.commit()
    emitRes(consts.TOP_HUMIDITY, consts.RESPONSE_OK, topicID)


def handle_message(topic, topicID, operation, payload, app):
    with app.app_context():
        match topic:
            case consts.TOP_PERMISSION_STATE:
                handle_permission_state(payload, operation, topicID)
                return
            case consts.TOP_IR_STATE:
                handle_ir_state(payload, operation, topicID)
                return
            case consts.TOP_PASSWORD:
                handle_password(payload, operation, topicID)
                return
            case consts.TOP_FREQUENCY:
                handle_frequency(payload, operation, topicID)
                return
            case consts.TOP_TEMPERATURE:
                handle_temperature(payload, operation, topicID)
                return
            case consts.TOP_HUMIDITY:
                handle_humidity(payload, operation, topicID)
                return
            case _:
                print("Unknown topic")
                return
