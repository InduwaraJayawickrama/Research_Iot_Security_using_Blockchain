import time
import random
from blockchain_layer.lightweight_pos import LightweightPoS
from blockchain_layer.blockchain import Blockchain

class ConsensusComparator:
    def __init__(self):
        self.validators = {
            "v1": 100,
            "v2": 150,
            "v3": 80,
            "v4": 120,
            "v5": 90
        }
    
    def test_pos(self, num_blocks=100):
        """Test Proof of Stake performance"""
        blockchain = Blockchain()
        start_time = time.time()
        
        for i in range(num_blocks):
            # Simulate block creation
            time.sleep(0.01)
        
        elapsed = time.time() - start_time
        return {
            "time": elapsed,
            "tps": num_blocks / elapsed
        }
    
    def test_pow(self, num_blocks=100):
        """Simulate Proof of Work performance"""
        blockchain = Blockchain()
        start_time = time.time()
        
        for i in range(num_blocks):
            # Simulate mining delay
            time.sleep(0.1)
        
        elapsed = time.time() - start_time
        return {
            "time": elapsed,
            "tps": num_blocks / elapsed
        }
    
    def test_raft(self, num_blocks=100):
        """Simulate Raft consensus performance"""
        blockchain = Blockchain()
        start_time = time.time()
        
        for i in range(num_blocks):
            # Simulate leader election and replication
            time.sleep(0.05)
        
        elapsed = time.time() - start_time
        return {
            "time": elapsed,
            "tps": num_blocks / elapsed
        }
    
    def compare_consensus(self, num_blocks=100):
        return {
            "PoS": self.test_pos(num_blocks),
            "PoW": self.test_pow(num_blocks),
            "Raft": self.test_raft(num_blocks)
        }