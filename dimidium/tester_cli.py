import paho.mqtt.client as mqtt 
import time
import json
import utils
import random

def onConnect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code: '{rc}'")
    client.subscribe([
        (utils.TOP_PERMISSION_STATE, utils.TOPICS_QOS),
        (utils.TOP_IR_STATE, utils.TOPICS_QOS),
        (utils.TOP_PASSWORD, utils.TOPICS_QOS),
        (utils.TOP_FREQUENCY, utils.TOPICS_QOS)
    ])

def readDB(key):
    with open(utils.DB_PATH, "r") as file:
        dbObj = json.load(file)
        return dbObj[key]

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)

client.on_connect = onConnect

client.connect(utils.BROKER_URL, port=utils.BROKER_PORT)

def permissionState():
    print("Permission state")

def irState():
    while True:
        print("\n------------ IR STATE ------------ ")
        print("1. Close")
        print("2. Open")
        print("3. Ping every 2 seconds")
        print("4. Go back")

        choice = input("\nEnter your choice: ")

        match choice:
            case "1":
                client.publish(utils.TOP_IR_STATE, "0")
            case "2":
                client.publish(utils.TOP_IR_STATE, "1")
            case "3":
                while True:
                    print("\n------------ PING TYPE ------------ ")
                    print("1. Close")
                    print("2. Open")
                    print("3. Random")
                    print("4. Go back")

                    choice = input("\nEnter your choice: ")

                    match choice:
                        case "1":
                            while True:
                                client.publish(utils.TOP_IR_STATE, "0")
                                print("Message '0' sent, waiting for 2 seconds. Press 'CTRL+C' to kill the CLI")
                                time.sleep(2)
                        case "2":
                            while True:
                                client.publish(utils.TOP_IR_STATE, "1")
                                print("Message '1' sent, waiting for 2 seconds. Press 'CTRL+C' to kill the CLI")
                                time.sleep(2)
                        case "3":
                            while True:
                                s = random.choice(["0", "1"])
                                client.publish(utils.TOP_IR_STATE, s)
                                print(f"Message '{s}' sent, waiting for 2 seconds. Press 'CTRL+C' to kill the CLI")
                                time.sleep(2)
                        case "4":
                            break
            case "4":
                break
            case _:
                print("\nInvalid choice")

def password():
    print("Password")

def frequency():
    print("Frequency")

while True:
    print("\n------------ MQTT TESTING CLI ------------ ")

    while True:
        print("\n------------ CURRENT VALUES ------------ ")
        print(f"Permission State: {'ALLOWED' if readDB(utils.TOP_PERMISSION_STATE)['value'] == 'true' else 'PROHIBITED'}")
        print(f"IR State: {'OPEN' if readDB(utils.TOP_IR_STATE)['value'] == '1' else 'CLOSED'}")
        print(f"Password: {readDB(utils.TOP_PASSWORD)['value']}")
        print(f"Frequency: {readDB(utils.TOP_FREQUENCY)['value']}")

        print("\n------------ OPTIONS ------------ ")

        print("1. Permission State")
        print("2. IR State")
        print("3. Password")
        print("4. Frequency")
        print("5. Quit")

        choice = input("\nEnter your choice: ")
        
        match choice:
            case "1":
                permissionState()
            case "2":
                irState()
            case "3":
                password()
            case "4":
                frequency()
            case "5":
                exit()
            case _:
                print("\nInvalid choice")

