from .block import Block
from .blockchain_interface import BlockchainInterface
from .lightweight_pos import LightweightPoS
import config

class Blockchain(BlockchainInterface):
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.consensus = LightweightPoS(config.VALIDATOR_STAKES)
    
    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0", "system")
    
    def add_block(self, data, validator_id):
        if not self.consensus.is_valid_validator(validator_id):
            raise ValueError(f"Invalid validator: {validator_id}")
        
        latest_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            data=data,
            previous_hash=latest_block.hash,
            validator=validator_id
        )
        self.chain.append(new_block)
        return new_block
    
    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Validate hash integrity
            if current.hash != current.calculate_hash():
                return False
                
            # Validate chain linkage
            if current.previous_hash != previous.hash:
                return False
                
            # Validate block creator
            if not self.consensus.is_valid_validator(current.validator):
                return False
                
        return True

    def get_latest_block(self):
        return self.chain[-1]

    def get_chain(self):
        return [block.to_dict() for block in self.chain]