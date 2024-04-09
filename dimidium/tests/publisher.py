import paho.mqtt.client as mqtt 
import time
 
BROKER_URL = "test.mosquitto.org" 
BROKER_PORT = 1883

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
client.connect(BROKER_URL, port=BROKER_PORT)

while True:
    client.publish("IR_STATE", '0')
    time.sleep(5)
    client.publish("IR_STATE", '1')
    time.sleep(5)
    client.publish("PERMISSION_STATE", '1')
    time.sleep(5)
