import unittest
from fog_layer.validator import ValidatorNode
from fog_layer.security_monitor import SecurityMonitor

class TestFogLayer(unittest.TestCase):
    def test_security_monitor(self):
        monitor = SecurityMonitor()
        
        # Valid transaction
        valid_tx = {
            "device_id": "sensor1",
            "data": {"type": "temperature", "value": 25.5},
            "signature": "valid_signature_123456"
        }
        self.assertFalse(monitor.check_transaction(valid_tx))
        
        # Invalid transaction (temperature out of range)
        invalid_tx = {
            "device_id": "sensor1",
            "data": {"type": "temperature", "value": 100},
            "signature": "invalid"
        }
        self.assertTrue(monitor.check_transaction(invalid_tx))

if __name__ == '__main__':
    unittest.main()