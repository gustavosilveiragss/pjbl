import paho.mqtt.client as mqtt
import time

def sub_temperatura(client, userdata, message):
    print("Tópico: ", str(message.topic))
    print("Msg: " ,str(message.payload.decode("utf-8")))

mqttBroker = "broker.emqx.io" 

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(mqttBroker, 1883) 

client.message_callback_add("top1", sub_temperatura)
client.subscribe("top1")

client.loop_forever()
