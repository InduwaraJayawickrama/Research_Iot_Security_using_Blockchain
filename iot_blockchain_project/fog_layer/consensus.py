import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blockchain_layer.lightweight_pos import LightweightPoS
import config
import hashlib

class ConsensusManager:
    def __init__(self):
        self.pos = LightweightPoS(config.VALIDATOR_STAKES)
        self.current_validator = self.pos.select_validator("genesis")
    
    def get_validator(self):
        return self.current_validator
    
    def rotate_validator(self, previous_block_hash):
        self.current_validator = self.pos.rotate_validator(self.current_validator)
        return self.current_validator
    
    def validate_block(self, block, previous_block):
        # Validate hash chain
        if block.previous_hash != previous_block.hash:
            return False
        
        # Validate block hash
        if block.hash != block.calculate_hash():
            return False
        
        # Validate validator
        if not self.pos.is_valid_validator(block.validator):
            return False
        
        return True