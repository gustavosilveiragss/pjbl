device = [
    dict(
        device_id=1,
        created_at="2024-05-01 00:00:00",
        device_name="Halux",
        password="",
        permission_state=0,
    ),
    dict(
        device_id=2,
        created_at="2024-05-01 00:00:00",
        device_name="Test Box",
        password="000",
        permission_state=0,
    ),
]

sensor_model = [
    dict(
        sensor_model_id=1,
        created_at="2024-05-01 00:00:00",
        name="DHT22 - Temperature",
    ),
    dict(
        sensor_model_id=2,
        created_at="2024-05-01 00:00:00",
        name="DHT22 - Humidity",
    ),
    dict(
        sensor_model_id=3,
        created_at="2024-05-01 00:00:00",
        name="TCRT5000",
    ),
]

actuator_model = [
    dict(
        actuator_model_id=1,
        created_at="2024-05-01 00:00:00",
        name="Button",
    ),
    dict(
        actuator_model_id=2,
        created_at="2024-05-01 00:00:00",
        name="Buzzer",
    ),
]

device_sensor = [
    dict(device_id=2, sensor_model_id=1, updated_at="2024-05-01 00:00:00", value=25),
    dict(device_id=2, sensor_model_id=2, updated_at="2024-05-01 00:00:00", value=50),
    dict(device_id=2, sensor_model_id=3, updated_at="2024-05-01 00:00:00", value=1),
]

device_actuator = [
    dict(device_id=2, actuator_model_id=1, updated_at="2024-05-01 00:00:00", value=0),
    dict(device_id=2, actuator_model_id=2, updated_at="2024-05-01 00:00:00", value=800),
]

user = [
    dict(
        user_id=1,
        created_at="2024-05-01 00:00:00",
        username="admin",
        password="admin",
    ),
    dict(
        user_id=2,
        created_at="2024-05-01 00:00:00",
        username="user",
        password="user",
    ),
]

mqtt_logs = [
    dict(
        mqtt_log_id=1,
        created_at="2024-05-01 00:00:00",
        topic="PERMISSION_STATE",
        subtopic="CRUD",
        device_id=2,
        operation="C",
        payload="1",
    ),
    dict(
        mqtt_log_id=2,
        created_at="2024-05-01 00:00:00",
        topic="IR_STATE",
        subtopic="REQ",
        device_id=2,
        operation="W",
        payload="1",
    ),
    dict(
        mqtt_log_id=3,
        created_at="2024-05-01 00:00:00",
        topic="PASSWORD",
        subtopic="REQ",
        device_id=2,
        operation="W",
        payload="000",
    ),
    dict(
        mqtt_log_id=4,
        created_at="2024-05-01 00:00:00",
        topic="FREQUENCY",
        subtopic="REQ",
        device_id=2,
        operation="W",
        payload="100",
    ),
    dict(
        mqtt_log_id=5,
        created_at="2024-05-01 00:00:00",
        topic="TEMPERATURE",
        subtopic="REQ",
        device_id=2,
        operation="W",
        payload="25",
    ),
    dict(
        mqtt_log_id=6,
        created_at="2024-05-01 00:00:00",
        topic="HUMIDITY",
        subtopic="REQ",
        device_id=2,
        operation="W",
        payload="30",
    ),
]
