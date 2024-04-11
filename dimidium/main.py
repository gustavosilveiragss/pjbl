import paho.mqtt.client as mqtt
import utils
from handler import handleMessage
from datetime import datetime

def onConnect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code: '{rc}'")
    client.subscribe(utils.SUBSCRIBE)

def onDisconnect(client, userdata, rc):
    print(f"Disconnected with result code: '{rc}'")

def onMessage(client, userdata, message):
    path = message.topic.split('/')

    topic = path[0]
    subtopic = path[1]
    topicID = path[2]

    if subtopic == utils.REQUEST:
        operation = path[3]
    else:
        operation = utils.RESPONSE

    payload = message.payload.decode("utf-8")
    
    print(f"Time: {datetime.now()} | Topic: {topic} | Subtopic: {subtopic} | Topic ID: {topicID} | Operation: {operation} | Payload: {payload}")

    if subtopic == utils.REQUEST:
        handleMessage(client, topic, topicID, operation, payload)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5, client_id=utils.genID())

client.on_connect = onConnect
client.on_disconnect = onDisconnect
client.on_message = onMessage

client.connect(utils.BROKER_URL, port=utils.BROKER_PORT)

client.loop_forever()
