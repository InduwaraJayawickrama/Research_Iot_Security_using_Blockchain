import unittest
from blockchain_layer.blockchain import Blockchain
from blockchain_layer.lightweight_pos import LightweightPoS

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
    
    def test_genesis_block(self):
        genesis = self.blockchain.chain[0]
        self.assertEqual(genesis.index, 0)
        self.assertEqual(genesis.data, "Genesis Block")
    
    def test_add_block(self):
        self.blockchain.add_block("Test Data", "validator1")
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(self.blockchain.chain[1].data, "Test Data")
    
    def test_chain_validation(self):
        self.blockchain.add_block("Data1", "validator1")
        self.blockchain.add_block("Data2", "validator2")
        self.assertTrue(self.blockchain.validate_chain())
        
        # Tamper with chain
        self.blockchain.chain[1].data = "Tampered Data"
        self.assertFalse(self.blockchain.validate_chain())

if __name__ == '__main__':
    unittest.main()