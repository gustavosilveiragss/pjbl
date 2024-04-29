import utils.consts as consts
from flask_mqtt import Mqtt
from models.db import db

mqtt_client = Mqtt()

topics_subscribe = [
    consts.TOP_PERMISSION_STATE + "/#",
    consts.TOP_IR_STATE + "/#",
    consts.TOP_PASSWORD + "/#",
    consts.TOP_FREQUENCY + "/#",
    consts.TOP_TEMPERATURE + "/#",
    consts.TOP_HUMIDITY + "/#"
]

def returnError(msg):
    return '{"status": "ERROR", "message": "' + msg + '"}'

def emitRes(topic, payload, id):
    mqtt_client.publish(f'{topic}/{consts.RESPONSE}/{id}', payload)

def handlePermissionState(client, payload, operation, topicID):
    if operation == consts.READ:
        res = "ALLOWED" if db.readDB(consts.TOP_PERMISSION_STATE)['value'] == "true" else "PROHIBITED"
        emitRes(consts.TOP_PERMISSION_STATE, res, topicID)
        return
    
    if payload != "true" and payload != "false":
        emitRes(consts.TOP_PERMISSION_STATE, returnError("Permission state must be either 'true' or 'false'"), topicID)
        return

    consts.writeDB(consts.TOP_PERMISSION_STATE, payload)
    emitRes(consts.TOP_PERMISSION_STATE, consts.RESPONSE_OK, topicID)

def handleIRState(client, payload, operation, topicID):
    if operation == consts.READ:
        res = "OPEN" if db.readDB(consts.TOP_IR_STATE)['value'] == "1" else "CLOSED"
        emitRes(consts.TOP_IR_STATE, res, topicID)
        return
    
    if payload != "0" and payload != "1":
        emitRes(consts.TOP_IR_STATE, returnError("IR state must be either '0' or '1'"), topicID)
        return

    consts.writeDB(consts.TOP_IR_STATE, payload)
    emitRes(consts.TOP_IR_STATE, consts.RESPONSE_OK, topicID)

def handlePassword(client, payload, operation, topicID):
    if operation == consts.READ:
        emitRes(consts.TOP_PASSWORD, db.readDB(consts.TOP_PASSWORD)['value'], topicID)
        return
    
    if len(payload) != 3:
        emitRes(consts.TOP_PASSWORD, returnError("Password sequence must be 3 characters long"), topicID)
        return
    
    for i in payload:
        if not i.isdigit() or int(i) < 0 or int(i) > 2:
            emitRes(consts.TOP_PASSWORD, returnError("Password sequence must contain only numbers between 0 and 2"), topicID)
            return

    consts.writeDB(consts.TOP_PASSWORD, payload)
    emitRes(consts.TOP_PASSWORD, consts.RESPONSE_OK, topicID)

def handleFrequency(client, payload, operation, topicID):
    if operation == consts.READ:
        emitRes(consts.TOP_FREQUENCY, db.readDB(consts.TOP_FREQUENCY)['value'], topicID)
        return
    
    if not payload.isdigit() or int(payload) < 0 or int(payload) > 10000:
        emitRes(consts.TOP_FREQUENCY, returnError("Frequency must be a number between 0 and 10000"), topicID)
        return
    
    consts.writeDB(consts.TOP_FREQUENCY, payload)
    emitRes(consts.TOP_FREQUENCY, consts.RESPONSE_OK, topicID)

def handleTemperature(client, payload, operation, topicID):
    if operation == consts.READ:
        emitRes(consts.TOP_TEMPERATURE, db.readDB(consts.TOP_TEMPERATURE)['value'], topicID)
        return
    
    def validateTemperature():
        try:
            return float(payload) >= 0 and float(payload) <= 100
        except ValueError:
            return False
    
    if not validateTemperature():
        emitRes(consts.TOP_TEMPERATURE, returnError("Temperature must be a number between 0.0 and 100.0, indicating the degrees celsius"), topicID)
        return
    
    consts.writeDB(consts.TOP_TEMPERATURE, payload)
    emitRes(consts.TOP_TEMPERATURE, consts.RESPONSE_OK, topicID)

def handleHumidity(client, payload, operation, topicID):
    if operation == consts.READ:
        emitRes(consts.TOP_HUMIDITY, db.readDB(consts.TOP_HUMIDITY)['value'], topicID)
        return
    
    def validateHumidity():
        try:
            return float(payload) >= 0 and float(payload) <= 100
        except ValueError:
            return False
    
    if not validateHumidity():
        emitRes(consts.TOP_HUMIDITY, returnError("Humidity must be a number between 0.0 and 100.0, indicating the humidity percentage"), topicID)
        return
    
    consts.writeDB(consts.TOP_HUMIDITY, payload)
    emitRes(consts.TOP_HUMIDITY, consts.RESPONSE_OK, topicID)

def handleMessage(client, topic, topicID, operation, payload):
    match topic:
        case consts.TOP_PERMISSION_STATE:
            handlePermissionState(client, payload, operation, topicID)
            return
        case consts.TOP_IR_STATE:
            handleIRState(client, payload, operation, topicID)
            return
        case consts.TOP_PASSWORD:
            handlePassword(client, payload, operation, topicID)
            return
        case consts.TOP_FREQUENCY:
            handleFrequency(client, payload, operation, topicID)
            return
        case consts.TOP_TEMPERATURE:
            handleTemperature(client, payload, operation, topicID)
            return
        case consts.TOP_HUMIDITY:
            handleHumidity(client, payload, operation, topicID)
            return
        case _:
            print("Unknown topic")
            return