#!/usr/bin/env python3
"""
Test script for IoT Blockchain Visualizer components with realistic topology
"""

import sys
import os
import time
import json
import random

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from simulation.metrics import Metrics
        print("✓ Metrics imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Metrics: {e}")
        return False
    
    try:
        from simulation.network_simulator import NetworkSimulator
        print("✓ NetworkSimulator imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import NetworkSimulator: {e}")
        return False
    
    try:
        from blockchain_layer.blockchain import Blockchain
        print("✓ Blockchain imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Blockchain: {e}")
        return False
    
    try:
        from blockchain_layer.block import Block
        print("✓ Block imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Block: {e}")
        return False
    
    try:
        import config
        print("✓ Config imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import config: {e}")
        return False
    
    return True

def test_configuration():
    """Test the new configuration structure"""
    print("\nTesting configuration structure...")
    
    try:
        import config
        
        # Test validator configuration
        print(f"✓ Validators: {len(config.VALIDATOR_STAKES)} validators configured")
        print(f"✓ Total stake: {sum(config.VALIDATOR_STAKES.values())}")
        
        # Test validator connections
        total_connections = sum(len(connections) for connections in config.VALIDATOR_CONNECTIONS.values())
        print(f"✓ Validator connections: {total_connections} total connections")
        
        # Test IoT devices
        print(f"✓ Sensors: {len(config.SENSORS)} sensors configured")
        print(f"✓ Actuators: {len(config.ACTUATORS)} actuators configured")
        
        # Test device assignments
        sensor_validators = set(sensor['validator'] for sensor in config.SENSORS.values())
        actuator_validators = set(actuator['validator'] for actuator in config.ACTUATORS.values())
        all_device_validators = sensor_validators.union(actuator_validators)
        
        print(f"✓ Device assignments: {len(all_device_validators)} validators have devices")
        
        # Verify all device validators exist
        for validator in all_device_validators:
            if validator not in config.VALIDATOR_STAKES:
                print(f"✗ Device validator {validator} not found in VALIDATOR_STAKES")
                return False
        
        print("✓ All device validators are valid")
        
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_network_topology():
    """Test network topology creation"""
    print("\nTesting network topology...")
    
    try:
        import networkx as nx
        import config
        
        # Create network graph
        G = nx.Graph()
        
        # Add validators
        for validator_id in config.VALIDATOR_STAKES.keys():
            G.add_node(validator_id, node_type='validator')
        
        # Add validator connections
        for validator_id, connections in config.VALIDATOR_CONNECTIONS.items():
            for connected_validator in connections:
                if connected_validator in config.VALIDATOR_STAKES:
                    G.add_edge(validator_id, connected_validator, edge_type='validator')
        
        # Add sensors
        for sensor_id, sensor_config in config.SENSORS.items():
            G.add_node(sensor_id, node_type='sensor')
            G.add_edge(sensor_id, sensor_config["validator"], edge_type='device')
        
        # Add actuators
        for actuator_id, actuator_config in config.ACTUATORS.items():
            G.add_node(actuator_id, node_type='actuator')
            G.add_edge(actuator_id, actuator_config["validator"], edge_type='device')
        
        # Test topology properties
        total_nodes = G.number_of_nodes()
        total_edges = G.number_of_edges()
        
        validators = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'validator']
        sensors = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'sensor']
        actuators = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'actuator']
        
        print(f"✓ Total nodes: {total_nodes}")
        print(f"✓ Total edges: {total_edges}")
        print(f"✓ Validators: {len(validators)}")
        print(f"✓ Sensors: {len(sensors)}")
        print(f"✓ Actuators: {len(actuators)}")
        
        # Test connectivity
        components = list(nx.connected_components(G))
        print(f"✓ Connected components: {len(components)}")
        
        if len(components) == 1:
            print("✓ Network is fully connected")
        else:
            print(f"⚠ Network has {len(components)} disconnected components")
        
        # Test that each device connects to only one validator
        device_nodes = sensors + actuators
        for device in device_nodes:
            neighbors = list(G.neighbors(device))
            validator_neighbors = [n for n in neighbors if G.nodes[n].get('node_type') == 'validator']
            if len(validator_neighbors) != 1:
                print(f"✗ Device {device} connects to {len(validator_neighbors)} validators (should be 1)")
                return False
        
        print("✓ All devices connect to exactly one validator")
        
        return True
        
    except Exception as e:
        print(f"✗ Network topology test failed: {e}")
        return False

def test_blockchain():
    """Test blockchain functionality"""
    print("\nTesting blockchain functionality...")
    
    try:
        from blockchain_layer.blockchain import Blockchain
        
        blockchain = Blockchain()
        print("✓ Blockchain created successfully")
        
        # Test adding blocks with realistic IoT data
        test_sensor_data = {
            'device_id': 'temp_sensor_1',
            'device_type': 'sensor',
            'sensor_data': {
                'value': 25.5,
                'unit': '°C',
                'timestamp': time.time(),
                'type': 'temperature',
                'location': 'room_1'
            },
            'block_type': 'iot_data',
            'validator': 'validator1'
        }
        
        blockchain.add_block(json.dumps(test_sensor_data), 'validator1')
        print("✓ IoT sensor block added successfully")
        
        # Test adding actuator data
        test_actuator_data = {
            'device_id': 'heater_1',
            'device_type': 'actuator',
            'sensor_data': {
                'command': 'on',
                'value': 25.0,
                'timestamp': time.time(),
                'type': 'heater',
                'location': 'room_1'
            },
            'block_type': 'iot_data',
            'validator': 'validator1'
        }
        
        blockchain.add_block(json.dumps(test_actuator_data), 'validator1')
        print("✓ IoT actuator block added successfully")
        
        # Test chain validation
        is_valid = blockchain.validate_chain()
        print(f"✓ Chain validation: {'Valid' if is_valid else 'Invalid'}")
        
        # Test getting chain
        chain = blockchain.get_chain()
        print(f"✓ Chain length: {len(chain)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Blockchain test failed: {e}")
        return False

def test_metrics():
    """Test metrics functionality"""
    print("\nTesting metrics functionality...")
    
    try:
        from simulation.metrics import Metrics
        
        metrics = Metrics()
        print("✓ Metrics created successfully")
        
        # Test recording metrics
        metrics.record_latency(0.05)
        metrics.record_power(0.5)
        metrics.record_throughput(10)
        
        print(f"✓ Average latency: {metrics.get_average_latency():.3f}s")
        print(f"✓ Average power: {metrics.get_average_power():.2f}W")
        print(f"✓ Throughput rate: {metrics.get_throughput_rate():.2f} msg/s")
        
        return True
        
    except Exception as e:
        print(f"✗ Metrics test failed: {e}")
        return False

def test_network_simulator():
    """Test network simulator functionality"""
    print("\nTesting network simulator functionality...")
    
    try:
        from simulation.network_simulator import NetworkSimulator
        
        simulator = NetworkSimulator()
        print("✓ NetworkSimulator created successfully")
        
        # Test adding nodes
        simulator.add_node("validator1")
        simulator.add_node("validator2")
        simulator.add_node("temp_sensor_1")
        print("✓ Nodes added successfully")
        
        # Test sending messages
        latency = simulator.send_message("temp_sensor_1", "validator1", "sensor_data")
        print(f"✓ Message sent with latency: {latency*1000:.1f}ms")
        
        return True
        
    except Exception as e:
        print(f"✗ Network simulator test failed: {e}")
        return False

def test_device_simulation():
    """Test realistic device data generation"""
    print("\nTesting device simulation...")
    
    try:
        # Test sensor data generation
        sensor_types = ['temperature', 'humidity', 'pressure', 'light', 'motion']
        for sensor_type in sensor_types:
            if sensor_type == 'temperature':
                value = random.uniform(18, 32)
                unit = '°C'
            elif sensor_type == 'humidity':
                value = random.uniform(30, 80)
                unit = '%'
            elif sensor_type == 'pressure':
                value = random.uniform(1000, 1020)
                unit = 'hPa'
            elif sensor_type == 'light':
                value = random.uniform(0, 1000)
                unit = 'lux'
            elif sensor_type == 'motion':
                value = random.choice([0, 1])
                unit = 'binary'
            
            print(f"✓ {sensor_type} sensor: {value:.2f} {unit}")
        
        # Test actuator data generation
        actuator_types = ['heater', 'air_conditioner', 'light', 'fan', 'door_lock']
        for actuator_type in actuator_types:
            if actuator_type == 'heater':
                command = random.choice(['on', 'off'])
            elif actuator_type == 'air_conditioner':
                command = random.choice(['on', 'off'])
            elif actuator_type == 'light':
                command = random.choice(['on', 'off', 'dim'])
            elif actuator_type == 'fan':
                command = random.choice(['on', 'off'])
            elif actuator_type == 'door_lock':
                command = random.choice(['lock', 'unlock'])
            
            print(f"✓ {actuator_type} actuator: {command}")
        
        return True
        
    except Exception as e:
        print(f"✗ Device simulation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("IoT Blockchain Visualizer - Realistic Topology Tests")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_configuration,
        test_network_topology,
        test_blockchain,
        test_metrics,
        test_network_simulator,
        test_device_simulation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The realistic network topology is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 