import unittest
from simulation.metrics import Metrics
from simulation.network_simulator import NetworkSimulator

class TestSimulation(unittest.TestCase):
    def test_metrics_tracking(self):
        metrics = Metrics()
        metrics.record_latency(0.05)
        metrics.record_latency(0.06)
        self.assertAlmostEqual(metrics.get_average_latency(), 0.055)
        
        metrics.record_power(1.2)
        metrics.record_power(1.3)
        self.assertAlmostEqual(metrics.get_average_power(), 1.25)
    
    def test_network_simulation(self):
        net = NetworkSimulator()
        net.add_node("node1")
        net.add_node("node2")
        net.add_connection("node1", "node2", 0.05)
        
        latency = net.send_message("node1", "node2", "test")
        self.assertGreaterEqual(latency, 0.01)
        self.assertEqual(len(net.latencies), 1)

if __name__ == '__main__':
    unittest.main()