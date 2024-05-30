import paho.mqtt.client as mqtt 
import time
import utils
import random

def permissionState():
    print("\n------------ PERMISSION STATE ------------ ")
    print("1. Allow")
    print("2. Prohibit")
    print("3. Go back")

    choice = input("\nEnter your choice: ")

    match choice:
        case "1":
            utils.emitReq(client, utils.TOP_PERMISSION_STATE, utils.WRITE, "1", callback=lambda msg: print(msg))
            permissionState()
        case "2":
            utils.emitReq(client, utils.TOP_PERMISSION_STATE, utils.WRITE, "0", callback=lambda msg: print(msg))
            permissionState()
        case "3":
            init_cli()
        case _:
            print("\nInvalid choice")
            permissionState()

def irState():
    print("\n------------ IR STATE ------------ ")
    print("1. Close")
    print("2. Open")
    print("3. Ping every 2 seconds")
    print("4. Go back")

    choice = input("\nEnter your choice: ")

    match choice:
        case "1":
            utils.emitReq(client, utils.TOP_IR_STATE, utils.WRITE, "0", callback=lambda msg: print(msg))
            irState()
        case "2":
            utils.emitReq(client, utils.TOP_IR_STATE, utils.WRITE, "1", callback=lambda msg: print(msg))
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
                        utils.emitReq(client, utils.TOP_IR_STATE, utils.WRITE, "0", callback=lambda msg: print(msg))
                        print("Waiting for 2 seconds. Press 'CTRL+C' to kill the CLI")
                        time.sleep(2)
                case "2":
                    while True:
                        utils.emitReq(client, utils.TOP_IR_STATE, utils.WRITE, "1", callback=lambda msg: print(msg))
                        print("Waiting for 2 seconds. Press 'CTRL+C' to kill the CLI")
                        time.sleep(2)
                case "3":
                    while True:
                        s = random.choice(["0", "1"])
                        utils.emitReq(client, utils.TOP_IR_STATE, utils.WRITE, s, callback=lambda msg: print(msg))
                        print("Waiting for 2 seconds. Press 'CTRL+C' to kill the CLI")
                        time.sleep(2)
                case "4":
                    irState()
                case _:
                    print("\nInvalid choice")
                    irState()
        case "4":
            init_cli()
        case _:
            print("\nInvalid choice")
            irState()

def password():
    print("\n------------ PASSWORD ------------ ")

    password = input("\nEntering new password sequences:\nInput it considering:\nindex = order;\nvalue = button position\nFor example, 020 would be pressing the first button -> third -> first\n\nInput your sequence: ")
    utils.emitReq(client, utils.TOP_PASSWORD, utils.WRITE, password, callback=lambda msg: print(msg))

    init_cli()

def frequency():
    print("\n------------ FREQUENCY ------------ ")

    frequency = input("\nInput the frequency in hertz: ")
    utils.emitReq(client, utils.TOP_FREQUENCY, utils.WRITE, frequency, callback=lambda msg: print(msg))

    init_cli()

def temperature():
    print("\n------------ TEMPERATURE ------------ ")

    temperature = input("\nInput the temperature in celsius: ")
    utils.emitReq(client, utils.TOP_TEMPERATURE, utils.WRITE, temperature, callback=lambda msg: print(msg))

    init_cli()

def humidity():
    print("\n------------ HUMIDITY ------------ ")

    humidity = input("\nInput the humidity in percentage: ")
    utils.emitReq(client, utils.TOP_HUMIDITY, utils.WRITE, humidity, callback=lambda msg: print(msg))

    init_cli()

def init_cli():
    print("\n------------ MQTT TESTING CLI ------------ ")

    print("\n------------ CURRENT DB VALUES ------------ ")
    utils.emitReq(client, utils.TOP_PERMISSION_STATE, utils.READ, '0', callback=lambda x: print(f"Permission State: {x}"))
    utils.emitReq(client, utils.TOP_IR_STATE, utils.READ, '0', callback=lambda x: print(f"IR State: {x}"))
    utils.emitReq(client, utils.TOP_PASSWORD, utils.READ, '0', callback=lambda x: print(f"Password: {x}"))
    utils.emitReq(client, utils.TOP_FREQUENCY, utils.READ, '0', callback=lambda x: print(f"Frequency: {x}"))
    utils.emitReq(client, utils.TOP_TEMPERATURE, utils.READ, '0', callback=lambda x: print(f"Temperature: {x}"))
    utils.emitReq(client, utils.TOP_HUMIDITY, utils.READ, '0', callback=lambda x: print(f"Humidity: {x}"))

    print("\n------------ OPTIONS ------------ ")

    print("1. Permission State")
    print("2. IR State")
    print("3. Password")
    print("4. Frequency")
    print("5. Temp")
    print("6. Humidity")
    print("7. Exit")

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
            temperature()
        case "6":
            humidity()
        case "7":
            exit()
        case _:
            print("\nInvalid choice")
            init_cli()
            return

client = mqtt.Client("2", protocol=mqtt.MQTTv5)

client.connect(utils.BROKER_URL, port=utils.BROKER_PORT)

init_cli()