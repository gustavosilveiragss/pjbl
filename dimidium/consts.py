import paho.mqtt.client as mqtt

BROKER_URL = "test.mosquitto.org"
BROKER_PORT = 1883

TOPICS_QOS = mqtt.SubscribeOptions(qos=1)

TOP_PERMISSION_STATE = "PERMISSION_STATE"
TOP_IR_STATE = "IR_STATE"
TOP_PASSWORD = "PASSWORD"
TOP_FREQUENCY = "FREQUENCY"