import paho.mqtt.client as mqtt 
import time
 
mqttBroker ="broker.emqx.io" 

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(mqttBroker, 1883) 

while True:
    client.publish("top1", '0')
    time.sleep(2)
    client.publish("top1", '1')
