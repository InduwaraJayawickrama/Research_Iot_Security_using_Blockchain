import paho.mqtt.client as mqtt
import json
import time

class MQTTClient:
    def __init__(self, broker, port, topic):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = mqtt.Client()
    
    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
    
    def publish(self, message):
        payload = json.dumps(message)
        self.client.publish(self.topic, payload)
    
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()