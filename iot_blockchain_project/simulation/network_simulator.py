import random
import time

class NetworkSimulator:
    def __init__(self):
        self.latencies = []
        self.node_connections = {}
    
    def add_node(self, node_id):
        self.node_connections[node_id] = []
    
    def add_connection(self, node1, node2, latency):
        self.node_connections[node1].append((node2, latency))
        self.node_connections[node2].append((node1, latency))
    
    def send_message(self, source, destination, message):
        # Simulate network latency
        latency = self.calculate_latency(source, destination)
        time.sleep(latency)
        self.latencies.append(latency)
        return latency
    
    def calculate_latency(self, source, destination):
        # Base latency + random variation
        base_latency = 0.05  # 50ms
        variation = random.uniform(-0.02, 0.03)
        return max(0.01, base_latency + variation)
    
    def simulate_network_load(self, nodes, duration=60, interval=1):
        end_time = time.time() + duration
        while time.time() < end_time:
            source, dest = random.sample(nodes, 2)
            self.send_message(source, dest, "test")
            time.sleep(interval)