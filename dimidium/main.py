import paho.mqtt.client as mqtt
import consts
from handler import handle_message
from datetime import datetime

def onConnect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code: '{rc}'")
    client.subscribe([
        (consts.TOP_PERMISSION_STATE, consts.TOPICS_QOS),
        (consts.TOP_IR_STATE, consts.TOPICS_QOS),
        (consts.TOP_PASSWORD, consts.TOPICS_QOS),
        (consts.TOP_FREQUENCY, consts.TOPICS_QOS)
    ])

def onDisconnect(client, userdata, rc):
    print(f"Disconnected with result code: '{rc}'")

def onMessage(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    
    print(f"Time: {datetime.now()} | Topic: {topic} | Payload: {payload}")

    handle_message(topic, payload)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)

client.on_connect = onConnect
client.on_disconnect = onDisconnect
client.on_message = onMessage

client.connect(consts.BROKER_URL, port=consts.BROKER_PORT)

client.loop_forever()
