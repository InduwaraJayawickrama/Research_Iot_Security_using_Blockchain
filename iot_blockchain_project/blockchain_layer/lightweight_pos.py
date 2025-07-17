import hashlib
import random

class LightweightPoS:
    def __init__(self, validators):
        self.validators = validators
        self.total_stake = sum(validators.values())
    
    def select_validator(self, previous_hash):
        """Stake-weighted validator selection with hash-based randomness"""
        seed = int(hashlib.sha256(previous_hash.encode()).hexdigest(), 16)
        random.seed(seed)
        selector = random.uniform(0, self.total_stake)
        cumulative = 0
        
        for validator, stake in self.validators.items():
            cumulative += stake
            if selector <= cumulative:
                return validator
    
    def is_valid_validator(self, validator_id):
        return validator_id in self.validators
    
    def rotate_validator(self, current_validator):
        """Rotate to next validator in weighted order"""
        validators_sorted = sorted(
            self.validators.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        try:
            current_index = [v[0] for v in validators_sorted].index(current_validator)
            next_index = (current_index + 1) % len(validators_sorted)
            return validators_sorted[next_index][0]
        except ValueError:
            return validators_sorted[0][0]