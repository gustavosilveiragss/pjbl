import json
import time
import paho.mqtt.client as mqtt
import os

BROKER_URL = "test.mosquitto.org"
BROKER_PORT = 1883

TOPICS_QOS = mqtt.SubscribeOptions(qos=1)

TOP_PERMISSION_STATE = "PERMISSION_STATE"
TOP_IR_STATE = "IR_STATE"
TOP_PASSWORD = "PASSWORD"
TOP_FREQUENCY = "FREQUENCY"

REQUEST = "REQ"
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

def emitReq(client, topic, payload, id=None):
    if id == None:
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
        message = json.loads(messageRaw)

        client.unsubscribe(f'{topic}/{RESPONSE}/{id}')
        received = True
        client.loop_stop()

        if message['status'] == 'ERROR':
            print(f"\nReceived error response '{message['message']}' on topic ID '{id}'")
            return
        
        print(f"\nReceived response 'OK' on topic ID '{id}'")

    client.publish(f'{topic}/{REQUEST}/{id}', payload)

    client.on_message = onMessage

    print(f"\nSent request for topic {topic}/{REQUEST}/{id}")

    while not received:
        if time.time() - time_start < 2:
            continue
        print(f"\nNo response received for topic ID '{id}'")
        client.loop_stop()
        break

def emitRes(client, topic, payload, id=None):
    if id == None:
        id = genID()
    client.publish(f'{topic}/{RESPONSE}/{id}', payload)

DB_PATH = os.path.abspath(os.path.dirname(__file__)) + "/data/db.json"
