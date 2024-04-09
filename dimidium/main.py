import paho.mqtt.client as mqtt
import utils
from handler import handleMessage
from datetime import datetime

def onConnect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code: '{rc}'")
    client.subscribe([
        (utils.TOP_PERMISSION_STATE, utils.TOPICS_QOS),
        (utils.TOP_IR_STATE, utils.TOPICS_QOS),
        (utils.TOP_PASSWORD, utils.TOPICS_QOS),
        (utils.TOP_FREQUENCY, utils.TOPICS_QOS)
    ])

def onDisconnect(client, userdata, rc):
    print(f"Disconnected with result code: '{rc}'")

def onMessage(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")
    
    print(f"Time: {datetime.now()} | Topic: {topic} | Payload: {payload}")

    handleMessage(topic, payload)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)

client.on_connect = onConnect
client.on_disconnect = onDisconnect
client.on_message = onMessage

client.connect(utils.BROKER_URL, port=utils.BROKER_PORT)

client.loop_forever()
