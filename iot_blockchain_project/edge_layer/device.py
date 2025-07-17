# Simulates an IoT device (sensor) 
import time
import json
import sys
import os
# Add the parent directory to the path to import from blockchain_layer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'blockchain_layer'))
# Add the parent directory to the path to import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from crypto_utils import generate_ecdsa_keys, sign_data, encrypt_aes
from mqtt_utils import MQTTClient
import config
# Pre-shared AES key (for demonstration, should be securely shared in practice)
AES_KEY = b'This is a key123'  # 16 bytes for AES-128
# Generate ECDSA keys for the device
private_key, public_key = generate_ecdsa_keys()
# MQTT client setup
mqtt_client = MQTTClient(config.MQTT_BROKER, config.MQTT_PORT, config.MQTT_TOPIC)
mqtt_client.connect()
# Simulate sensor data
sensor_id = "sensor_1"
while True:
    # Simulate reading sensor data (e.g., temperature)
    sensor_value = 25.0  # Replace with actual sensor reading
    data = {
        "sensor_id": sensor_id,
        "value": sensor_value,
        "timestamp": time.time()
    }
    data_str = json.dumps(data)
    # Sign the data
    signature = sign_data(private_key, data_str)
    # Encrypt the data
    encrypted_data, iv, tag = encrypt_aes(data_str, AES_KEY)
    # Prepare the message to send
    message = {
        "sensor_id": sensor_id,
        "encrypted_data": encrypted_data,
        "iv": iv,
        "tag": tag,
        "signature": signature
    }
    # Publish the message
    mqtt_client.publish(message)
    time.sleep(10)  # Send every 10 seconds