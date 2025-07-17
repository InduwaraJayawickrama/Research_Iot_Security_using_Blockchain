from abc import ABC, abstractmethod

class BlockchainInterface(ABC):
    @abstractmethod
    def add_block(self, data, validator_id):
        pass
    
    @abstractmethod
    def validate_chain(self):
        pass
    
    @abstractmethod
    def get_latest_block(self):
        pass
    
    @abstractmethod
    def get_chain(self):
        pass