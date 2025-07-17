# Configuration settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/data"

# Validator nodes with stakes and limited connectivity
VALIDATOR_STAKES = {
    "validator1": 100,
    "validator2": 150,
    "validator3": 80,
    "validator4": 120,
    "validator5": 90,
    "validator6": 110,
    "validator7": 75,
    "validator8": 130
}

# Validator network topology (which validators can communicate with each other)
VALIDATOR_CONNECTIONS = {
    "validator1": ["validator2", "validator3"],
    "validator2": ["validator1", "validator4", "validator5"],
    "validator3": ["validator1", "validator6"],
    "validator4": ["validator2", "validator7"],
    "validator5": ["validator2", "validator8"],
    "validator6": ["validator3", "validator7"],
    "validator7": ["validator4", "validator6", "validator8"],
    "validator8": ["validator5", "validator7"]
}

# IoT Devices configuration
SENSORS = {
    "temp_sensor_1": {"type": "temperature", "location": "room_1", "validator": "validator1"},
    "temp_sensor_2": {"type": "temperature", "location": "room_2", "validator": "validator2"},
    "temp_sensor_3": {"type": "temperature", "location": "room_3", "validator": "validator3"},
    "humidity_sensor_1": {"type": "humidity", "location": "room_1", "validator": "validator1"},
    "humidity_sensor_2": {"type": "humidity", "location": "room_2", "validator": "validator4"},
    "pressure_sensor_1": {"type": "pressure", "location": "outdoor", "validator": "validator5"},
    "light_sensor_1": {"type": "light", "location": "room_1", "validator": "validator6"},
    "light_sensor_2": {"type": "light", "location": "room_2", "validator": "validator7"},
    "motion_sensor_1": {"type": "motion", "location": "entrance", "validator": "validator8"},
    "motion_sensor_2": {"type": "motion", "location": "corridor", "validator": "validator3"}
}

ACTUATORS = {
    "heater_1": {"type": "heater", "location": "room_1", "validator": "validator1"},
    "heater_2": {"type": "heater", "location": "room_2", "validator": "validator2"},
    "ac_1": {"type": "air_conditioner", "location": "room_1", "validator": "validator4"},
    "ac_2": {"type": "air_conditioner", "location": "room_3", "validator": "validator5"},
    "light_1": {"type": "light", "location": "room_1", "validator": "validator6"},
    "light_2": {"type": "light", "location": "room_2", "validator": "validator7"},
    "fan_1": {"type": "fan", "location": "room_1", "validator": "validator8"},
    "fan_2": {"type": "fan", "location": "room_3", "validator": "validator3"},
    "door_lock_1": {"type": "door_lock", "location": "entrance", "validator": "validator1"},
    "door_lock_2": {"type": "door_lock", "location": "back_door", "validator": "validator2"}
}

SECURITY_THRESHOLDS = {
    'signature_fail': 5,
    'data_tamper': 3,
    'connection_timeout': 30,
    'max_data_rate': 100  # messages per minute per device
}

# Network simulation parameters
NETWORK_CONFIG = {
    'base_latency': 0.05,  # 50ms base latency
    'latency_variation': 0.02,  # ±20ms variation
    'packet_loss_rate': 0.01,  # 1% packet loss
    'bandwidth_limit': 1000,  # messages per second
    'connection_timeout': 30  # seconds
}