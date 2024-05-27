-- MySQL 
CREATE TABLE IF NOT EXISTS `user` (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `role` VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    `password` VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS device (
    device_id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
CREATE TABLE IF NOT EXISTS sensor_model (
    sensor_model_id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `name` VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS device_sensor (
    device_sensor_id INT AUTO_INCREMENT PRIMARY KEY,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    device_id INT NOT NULL,
    sensor_model_id INT NOT NULL,
    `value` VARCHAR(255) NOT NULL,
    FOREIGN KEY (device_id) REFERENCES device(device_id),
    FOREIGN KEY (sensor_model_id) REFERENCES sensor_model(sensor_model_id)
);
CREATE TABLE IF NOT EXISTS actuator_model (
    actuator_model_id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `name` VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS device_actuator (
    device_actuator_id INT AUTO_INCREMENT PRIMARY KEY,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    device_id INT NOT NULL,
    actuator_model_id INT NOT NULL,
    `value` VARCHAR(255) NOT NULL,
    FOREIGN KEY (device_id) REFERENCES device(device_id),
    FOREIGN KEY (actuator_model_id) REFERENCES actuator_model(actuator_model_id)
);
CREATE TABLE IF NOT EXISTS mqtt_logs (
    mqtt_log_id INT AUTO_INCREMENT PRIMARY KEY,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    topic VARCHAR(255) NOT NULL,
    subtopic VARCHAR(255) NOT NULL,
    device_id INT NOT NULL,
    operation VARCHAR(255) NOT NULL,
    payload VARCHAR(255) NOT NULL,
    FOREIGN KEY (device_id) REFERENCES device(device_id)
);
-- INDEXES
CREATE INDEX idx_user_username ON user(username);
CREATE INDEX idx_device_user_id ON device(user_id);
CREATE INDEX idx_sensor_model_name ON sensor_model(`name`);
CREATE INDEX idx_device_sensor_device_id ON device_sensor(device_id);
CREATE INDEX idx_device_sensor_sensor_model_id ON device_sensor(sensor_model_id);
CREATE INDEX idx_actuator_model_name ON actuator_model(`name`);
CREATE INDEX idx_device_actuator_device_id ON device_actuator(device_id);
CREATE INDEX idx_device_actuator_actuator_model_id ON device_actuator(actuator_model_id);
CREATE INDEX idx_mqtt_logs_device_id ON mqtt_logs(device_id);
CREATE INDEX idx_mqtt_logs_topic ON mqtt_logs(topic);
CREATE INDEX idx_mqtt_logs_subtopic ON mqtt_logs(subtopic);
-- DATA
-- device
INSERT INTO device (device_id, created_at, user_id)
VALUES (1, '2024-05-01 00:00:00', 1),
    (2, '2024-05-01 00:00:00', 2);
-- sensor_model
INSERT INTO sensor_model (sensor_model_id, created_at, `name`)
VALUES (1, '2024-05-01 00:00:00', 'DHT22 - Temperature'),
    (2, '2024-05-01 00:00:00', 'DHT22 - Humidity'),
    (3, '2024-05-01 00:00:00', 'TCRT5000');
-- actuator_model
INSERT INTO actuator_model (actuator_model_id, created_at, `name`)
VALUES (1, '2024-05-01 00:00:00', 'Button'),
    (2, '2024-05-01 00:00:00', 'Buzzer');
-- device_sensor
INSERT INTO device_sensor (device_id, sensor_model_id, updated_at, `value`)
VALUES (2, 1, '2024-05-01 00:00:00', 25),
    (2, 2, '2024-05-01 00:00:00', 50),
    (2, 3, '2024-05-01 00:00:00', 1);
-- device_actuator
INSERT INTO device_actuator (device_id, actuator_model_id, updated_at, `value`)
VALUES (2, 1, '2024-05-01 00:00:00', 0),
    (2, 2, '2024-05-01 00:00:00', 800);
-- user
INSERT INTO `user` (
        user_id,
        created_at,
        `role`,
        username,
        `password`
    )
VALUES (
        1,
        '2024-05-01 00:00:00',
        'admin',
        'admin',
        'admin'
    ),
    (2, '2024-05-01 00:00:00', 'user', 'user', 'user');
-- mqtt_logs
INSERT INTO mqtt_logs (
        mqtt_log_id,
        created_at,
        topic,
        subtopic,
        device_id,
        operation,
        payload
    )
VALUES (
        1,
        '2024-05-01 00:00:00',
        'PERMISSION_STATE',
        'REQ',
        2,
        'W',
        '1'
    ),
    (
        2,
        '2024-05-01 00:00:00',
        'IR_STATE',
        'REQ',
        2,
        'W',
        '1'
    ),
    (
        3,
        '2024-05-01 00:00:00',
        'PASSWORD',
        'REQ',
        2,
        'W',
        '000'
    ),
    (
        4,
        '2024-05-01 00:00:00',
        'FREQUENCY',
        'REQ',
        2,
        'W',
        '100'
    ),
    (
        5,
        '2024-05-01 00:00:00',
        'TEMPERATURE',
        'REQ',
        2,
        'W',
        '25'
    ),
    (
        6,
        '2024-05-01 00:00:00',
        'HUMIDITY',
        'REQ',
        2,
        'W',
        '30'
    );