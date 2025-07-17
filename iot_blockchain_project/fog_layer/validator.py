import json
import time
import sys
import os
import paho.mqtt.client as mqtt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blockchain_db import add_block, get_latest_block, init_db
from consensus import ConsensusManager
from security_monitor import SecurityMonitor
from blockchain_layer.crypto_utils import decrypt_aes, verify_signature
import config

# Pre-shared AES key (same as edge devices)
AES_KEY = b'16byteSecureKey123'

class ValidatorNode:
    def __init__(self, node_id):
        self.node_id = node_id
        # Initialize database
        init_db()
        # Create genesis block if none exists
        if get_latest_block() is None:
            genesis_block = {
                "index": 0,
                "timestamp": time.time(),
                "data": {"message": "Genesis Block"},
                "previous_hash": "0",
                "hash": "genesis_hash",
                "validator": "genesis"
            }
            add_block(genesis_block)
            print("Created genesis block")
        
        self.consensus = ConsensusManager()
        self.security_monitor = SecurityMonitor()
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(config.MQTT_BROKER, config.MQTT_PORT)
        self.mqtt_client.subscribe(config.MQTT_TOPIC)
    
    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload)
            device_id = payload["device_id"]
            encrypted_data = payload["encrypted_data"]
            nonce = payload["nonce"]
            tag = payload["tag"]
            signature = payload["signature"]
            
            # Decrypt data
            data_str = decrypt_aes(encrypted_data, nonce, tag, AES_KEY)
            
            # Verify signature
            # In production, we'd look up device's public key
            if not self.security_monitor.check_transaction(payload):
                print(f"Security alert! Rejecting transaction from {device_id}")
                return
                
            # Process transaction
            data = json.loads(data_str)
            print(f"Received valid data from {device_id}: {data}")
            
            # Create new block if this validator is current
            if self.consensus.get_validator() == self.node_id:
                latest_block = get_latest_block()
                new_block = {
                    "index": latest_block["index"] + 1,
                    "timestamp": time.time(),
                    "data": data,
                    "previous_hash": latest_block["hash"],
                    "validator": self.node_id
                }
                add_block(new_block)
                print(f"Added new block: {new_block['index']}")
                
                # Rotate validator after block creation
                self.consensus.rotate_validator(latest_block["hash"])
            
        except Exception as e:
            print(f"Error processing message: {str(e)}")
    
    def start(self):
        self.mqtt_client.loop_forever()

# Example usage
if __name__ == "__main__":
    validator = ValidatorNode("validator1")
    validator.start()