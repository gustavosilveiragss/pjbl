import utils

def handlePermissionState(client, payload, operation, topicID):
    if operation == utils.READ:
        res = "ALLOWED" if utils.readDB(utils.TOP_PERMISSION_STATE)['value'] == "true" else "PROHIBITED"
        utils.emitRes(client, utils.TOP_PERMISSION_STATE, res, topicID)
        return
    
    if payload != "true" and payload != "false":
        utils.emitRes(client, utils.TOP_PERMISSION_STATE, utils.returnError("Permission state must be either 'true' or 'false'"), topicID)
        return

    utils.writeDB(utils.TOP_PERMISSION_STATE, payload)
    utils.emitRes(client, utils.TOP_PERMISSION_STATE, utils.RESPONSE_OK, topicID)

def handleIRState(client, payload, operation, topicID):
    if operation == utils.READ:
        res = "OPEN" if utils.readDB(utils.TOP_IR_STATE)['value'] == "1" else "CLOSED"
        utils.emitRes(client, utils.TOP_IR_STATE, res, topicID)
        return
    
    if payload != "0" and payload != "1":
        utils.emitRes(client, utils.TOP_IR_STATE, utils.returnError("IR state must be either '0' or '1'"), topicID)
        return

    utils.writeDB(utils.TOP_IR_STATE, payload)
    utils.emitRes(client, utils.TOP_IR_STATE, utils.RESPONSE_OK, topicID)

def handlePassword(client, payload, operation, topicID):
    if operation == utils.READ:
        utils.emitRes(client, utils.TOP_PASSWORD, utils.readDB(utils.TOP_PASSWORD)['value'], topicID)
        return
    
    if len(payload) != 3:
        utils.emitRes(client, utils.TOP_PASSWORD, utils.returnError("Password sequence must be 3 characters long"), topicID)
        return
    
    for i in payload:
        if not i.isdigit() or int(i) < 0 or int(i) > 2:
            utils.emitRes(client, utils.TOP_PASSWORD, utils.returnError("Password sequence must contain only numbers between 0 and 2"), topicID)
            return

    utils.writeDB(utils.TOP_PASSWORD, payload)
    utils.emitRes(client, utils.TOP_PASSWORD, utils.RESPONSE_OK, topicID)

def handleFrequency(client, payload, operation, topicID):
    if operation == utils.READ:
        utils.emitRes(client, utils.TOP_FREQUENCY, utils.readDB(utils.TOP_FREQUENCY)['value'], topicID)
        return
    
    if not payload.isdigit() or int(payload) < 0 or int(payload) > 10000:
        utils.emitRes(client, utils.TOP_FREQUENCY, utils.returnError("Frequency must be a number between 0 and 10000"), topicID)
        return
    
    utils.writeDB(utils.TOP_FREQUENCY, payload)
    utils.emitRes(client, utils.TOP_FREQUENCY, utils.RESPONSE_OK, topicID)

def handleMessage(client, topic, topicID, operation, payload):
    match topic:
        case utils.TOP_PERMISSION_STATE:
            handlePermissionState(client, payload, operation, topicID)
            return
        case utils.TOP_IR_STATE:
            handleIRState(client, payload, operation, topicID)
            return
        case utils.TOP_PASSWORD:
            handlePassword(client, payload, operation, topicID)
            return
        case utils.TOP_FREQUENCY:
            handleFrequency(client, payload, operation, topicID)
            return
        case _:
            print("Unknown topic")
            return