import consts
        
def permission_state(payload):
    print("Permission state")

def ir_state(payload):
    print("IR state")

def password(payload):
    print("Password")

def frequency(payload):
    print("Frequency")

def handle_message(topic, payload):
    match topic:
        case consts.TOP_PERMISSION_STATE:
            permission_state(payload)
            return
        case consts.TOP_IR_STATE:
            ir_state(payload)
            return
        case consts.TOP_PASSWORD:
            password(payload)
            return
        case consts.TOP_FREQUENCY:
            frequency(payload)
            return
        case _:
            print("Unknown topic")
            return