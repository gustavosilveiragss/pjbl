import utils
import json
from datetime import datetime

def readDB(key):
    with open(utils.DB_PATH, "r") as file:
        dbObj = json.load(file)
        return dbObj[key]['value']
    
def writeDB(key, payload):
    with open(utils.DB_PATH, "r") as file:
        dbObj = json.load(file)
        val = {
            "lastChanged": str(datetime.now()),
            "value": payload
        }
        dbObj[key] = val

    with open(utils.DB_PATH, "w") as file:
        json.dump(dbObj, file)

def handlePermissionState(client, payload, topicID):
    writeDB(utils.TOP_PERMISSION_STATE, payload)
    utils.emitRes(client, utils.TOP_PERMISSION_STATE, utils.RESPONSE_OK, id=topicID)

def handleIRState(client, payload, topicID):
    writeDB(utils.TOP_IR_STATE, payload)
    utils.emitRes(client, utils.TOP_IR_STATE, utils.RESPONSE_OK, id=topicID)

def handlePassword(client, payload, topicID):
    if len(payload) != 3:
        utils.emitRes(client, utils.TOP_PASSWORD, utils.returnError("Password sequence must be 3 characters long"), id=topicID)
        return
    
    for i in payload:
        if not i.isdigit() or int(i) < 0 or int(i) > 3:
            utils.emitRes(client, utils.TOP_PASSWORD, utils.returnError("Password sequence must contain only numbers between 0 and 3"), id=topicID)
            return

    writeDB(utils.TOP_PASSWORD, payload)
    utils.emitRes(client, utils.TOP_PASSWORD, utils.RESPONSE_OK, id=topicID)

def handleFrequency(client, payload, topicID):
    if not payload.isdigit() or int(payload) < 0 or int(payload) > 10000:
        utils.emitRes(client, utils.TOP_FREQUENCY, utils.returnError("Frequency must be a number between 0 and 10000"), id=topicID)
        return
    writeDB(utils.TOP_FREQUENCY, payload)
    utils.emitRes(client, utils.TOP_FREQUENCY, utils.RESPONSE_OK, id=topicID)

def handleMessage(client, topic, topicID, payload):
    match topic:
        case utils.TOP_PERMISSION_STATE:
            handlePermissionState(client, payload, topicID)
            return
        case utils.TOP_IR_STATE:
            handleIRState(client, payload, topicID)
            return
        case utils.TOP_PASSWORD:
            handlePassword(client, payload, topicID)
            return
        case utils.TOP_FREQUENCY:
            handleFrequency(client, payload, topicID)
            return
        case _:
            print("Unknown topic")
            return