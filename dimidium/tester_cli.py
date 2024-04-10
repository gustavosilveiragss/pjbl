import paho.mqtt.client as mqtt 
import time
import json
import utils
import random

def readDB(key):
    with open(utils.DB_PATH, "r") as file:
        dbObj = json.load(file)
        return dbObj[key]

def permissionState():
    print("Permission state")
    init_cli()

def irState():
    print("\n------------ IR STATE ------------ ")
    print("1. Close")
    print("2. Open")
    print("3. Ping every 2 seconds")
    print("4. Go back")

    choice = input("\nEnter your choice: ")

    match choice:
        case "1":
            utils.emitReq(client, utils.TOP_IR_STATE, "0")
            irState()
        case "2":
            utils.emitReq(client, utils.TOP_IR_STATE, "1")
            irState()
        case "3":
            print("\n------------ PING TYPE ------------ ")
            print("1. Close")
            print("2. Open")
            print("3. Random")
            print("4. Go back")

            choice = input("\nEnter your choice: ")

            match choice:
                case "1":
                    while True:
                        utils.emitReq(client, utils.TOP_IR_STATE, "0")
                        print("Waiting for 2 seconds. Press 'CTRL+C' to kill the CLI")
                        time.sleep(2)
                case "2":
                    while True:
                        client.publish(utils.TOP_IR_STATE, "1")
                        print("Waiting for 2 seconds. Press 'CTRL+C' to kill the CLI")
                        time.sleep(2)
                case "3":
                    while True:
                        s = random.choice(["0", "1"])
                        utils.emitReq(client, utils.TOP_IR_STATE, s)
                        print("Waiting for 2 seconds. Press 'CTRL+C' to kill the CLI")
                        time.sleep(2)
                case "4":
                    irState()
        case "4":
            init_cli()
        case _:
            print("\nInvalid choice")
            irState()

def password():
    print("\n------------ PASSWORD ------------ ")

    password = input("\nEntering new password sequences:\nInput it considering:\nindex = order;\nvalue = button position\nFor example, 020 would be pressing the first button -> third -> first\n\nInput your sequence: ")
    utils.emitReq(client, utils.TOP_PASSWORD, password)

    init_cli()

def frequency():
    print("Frequency")
    init_cli()

def init_cli():
    print("\n------------ MQTT TESTING CLI ------------ ")

    print("\n------------ CURRENT DB VALUES ------------ ")
    print(f"Permission State: {'ALLOWED' if readDB(utils.TOP_PERMISSION_STATE)['value'] == 'true' else 'PROHIBITED'}")
    print(f"IR State: {'OPEN' if readDB(utils.TOP_IR_STATE)['value'] == '1' else 'CLOSED'}")
    print(f"Password: {readDB(utils.TOP_PASSWORD)['value']}")
    print(f"Frequency: {readDB(utils.TOP_FREQUENCY)['value']}")

    print("\n------------ OPTIONS ------------ ")

    print("1. Permission State")
    print("2. IR State")
    print("3. Password")
    print("4. Frequency")
    print("5. Exit")

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
            init_cli()
            return

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5, client_id=utils.genID())

client.connect(utils.BROKER_URL, port=utils.BROKER_PORT)

init_cli()