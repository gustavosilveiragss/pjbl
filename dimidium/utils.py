from datetime import datetime
import json
import time
import paho.mqtt.client as mqtt
import os

BROKER_URL = "broker.hivemq.com"
BROKER_PORT = 1883

TOPICS_QOS = mqtt.SubscribeOptions(qos=1)

TOP_PERMISSION_STATE = "PERMISSION_STATE"
TOP_IR_STATE = "IR_STATE"
TOP_PASSWORD = "PASSWORD"
TOP_FREQUENCY = "FREQUENCY"

REQUEST = "REQ"
READ = "R"
WRITE = "W"
RESPONSE = "RES"

SUBSCRIBE = [
    (TOP_PERMISSION_STATE + '/#', TOPICS_QOS),
    (TOP_IR_STATE + '/#', TOPICS_QOS),
    (TOP_PASSWORD + '/#', TOPICS_QOS),
    (TOP_FREQUENCY + '/#', TOPICS_QOS),
]

RESPONSE_OK = '{"status": "OK"}'

def returnError(msg):
    return '{"status": "ERROR", "message": "' + msg + '"}'

def genID():
    return str(os.urandom(4).hex())

def emitReq(client, topic, operation, payload, callback=None):
    id = genID()

    # Clear previous thread
    client.loop_stop()
    client.loop_start()

    client.subscribe(f'{topic}/{RESPONSE}/{id}')

    time_start = time.time()
    received = False

    def onMessage(_client, userdata, message):
        nonlocal received

        _topic = message.topic.split('/')[0]
        _subtopic = message.topic.split('/')[1]
        _topicID = message.topic.split('/')[2]

        if _topic != topic or _subtopic != RESPONSE or _topicID != id:
            return

        messageRaw = message.payload.decode('utf-8')

        client.unsubscribe(f'{topic}/{RESPONSE}/{id}')
        received = True
        client.loop_stop()

        if operation == READ:
            callback(messageRaw)
            return 
        
        message = json.loads(messageRaw)

        if message['status'] == 'ERROR':
            callback(f"Received error response '{message['message']}' on topic ID '{id}'")
            return 
        
        callback(f"Received response 'OK' on topic ID '{id}'")

    client.publish(f'{topic}/{REQUEST}/{id}/{operation}', payload)

    client.on_message = onMessage

    while not received:
        if time.time() - time_start < 2:
            continue
        client.loop_stop()
        callback(f"No response received for topic ID '{id}'")
        return

def emitRes(client, topic, payload, id):
    client.publish(f'{topic}/{RESPONSE}/{id}', payload)

DB_PATH = os.path.abspath(os.path.dirname(__file__)) + "/data/db.json"

def readDB(key):
    with open(DB_PATH, "r") as file:
        dbObj = json.load(file)
        return dbObj[key]
    
def writeDB(key, payload):
    with open(DB_PATH, "r") as file:
        dbObj = json.load(file)
        val = {
            "lastChanged": str(datetime.now()),
            "value": payload
        }
        dbObj[key] = val

    with open(DB_PATH, "w") as file:
        json.dump(dbObj, file)
