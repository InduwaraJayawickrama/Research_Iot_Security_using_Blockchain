class AccessControl:
    def __init__(self, permissions):
        self.permissions = permissions
    
    def validate_transaction(self, device_id, action, data=None):
        if device_id not in self.permissions:
            return False
            
        allowed_actions = self.permissions[device_id]
        
        if action not in allowed_actions:
            return False
            
        # Domain-specific validation
        if 'medical' in allowed_actions:
            return self._validate_medical(data)
        elif 'agriculture' in allowed_actions:
            return self._validate_agriculture(data)
            
        return True
    
    def _validate_medical(self, data):
        required_fields = ['patient_id', 'data_type', 'encrypted']
        return all(field in data for field in required_fields)
    
    def _validate_agriculture(self, data):
        return 'location' in data and 'sensor_type' in data