import config

class SecurityMonitor:
    def __init__(self):
        self.counters = {k: 0 for k in config.SECURITY_THRESHOLDS}
    
    def check_transaction(self, transaction):
        # Check signature failures
        if not self._verify_signature(transaction):
            self.counters['signature_fail'] += 1
        
        # Check for data tampering
        if self._detect_anomalies(transaction):
            self.counters['data_tamper'] += 1
        
        # Check if thresholds exceeded
        for key, threshold in config.SECURITY_THRESHOLDS.items():
            if self.counters[key] > threshold:
                return True
        return False
    
    def _verify_signature(self, transaction):
        # In real implementation, verify the cryptographic signature
        # For simulation, we'll assume valid if signature exists
        return 'signature' in transaction and len(transaction['signature']) > 10
    
    def _detect_anomalies(self, transaction):
        # Simple anomaly detection - check for impossible values
        if 'data' in transaction and 'value' in transaction['data']:
            value = transaction['data']['value']
            if transaction['data']['type'] == 'temperature' and (value < -20 or value > 60):
                return True
            elif transaction['data']['type'] == 'humidity' and (value < 0 or value > 100):
                return True
        return False
    
    def get_status(self):
        status = []
        for key, count in self.counters.items():
            status.append(f"{key}: {count}/{config.SECURITY_THRESHOLDS[key]}")
        return " | ".join(status)
    
    def reset_counters(self):
        self.counters = {k: 0 for k in self.counters}