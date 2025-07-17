import unittest
from edge_layer.crypto_edge import generate_keys, sign_data
from edge_layer.resource_monitor import ResourceMonitor

class TestEdgeLayer(unittest.TestCase):
    def test_key_generation(self):
        private_key, public_key = generate_keys()
        self.assertIsNotNone(private_key)
        self.assertIsNotNone(public_key)
    
    def test_signature_verification(self):
        private_key, public_key = generate_keys()
        data = "Test message"
        signature = sign_data(private_key, data)
        
        # Verify with correct data
        self.assertTrue(verify_signature(public_key, data, signature))
        
        # Verify with wrong data
        self.assertFalse(verify_signature(public_key, "Wrong message", signature))
    
    def test_resource_monitoring(self):
        monitor = ResourceMonitor("sensor1")
        metrics = monitor.get_metrics()
        self.assertIn("cpu", metrics)
        self.assertIn("memory", metrics)
        self.assertIn("energy", metrics)
        self.assertGreaterEqual(metrics["energy"], 0)

if __name__ == '__main__':
    unittest.main()