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

def handleMessage(topic, payload):
    match topic:
        case utils.TOP_PERMISSION_STATE:
            writeDB(utils.TOP_PERMISSION_STATE, payload)
            return
        case utils.TOP_IR_STATE:
            writeDB(utils.TOP_IR_STATE, payload)
            return
        case utils.TOP_PASSWORD:
            writeDB(utils.TOP_PASSWORD, payload)
            return
        case utils.TOP_FREQUENCY:
            writeDB(utils.TOP_FREQUENCY, payload)
            return
        case _:
            print("Unknown topic")
            return