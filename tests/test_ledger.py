import unittest
from unittest import TestCase

from src.block import VoteInfo, Block
from src.ledger import Ledger, SpeculationTree


class TestLedger(TestCase):
    def setUp(self) -> None:
        self.priv_key = SigningKeygenerate.()
        self.pub_key = self.priv_key.verify_key

    def test_speculate_when_data_is_correct_return_new_state(self):
        prev_block_id = "Block_1"
        block_id = "Block_2"
        txns = "Transaction"
        state_id = Ledger.speculate(prev_block_id, block_id, txns)
        self.assertIsInstance(state_id, str)

    def test_tree(self):
        ledger = Ledger()
        blocks = []
        for i in range(10):
            blocks.append(Block(f'Client-{i+1}', i, f'ClientSent-{i+1}', None, block_id=str(i)))
            
        ledger.speculate('GENESYS', blocks[0].block_id, blocks[0].payload)
        ledger.speculate('0', blocks[1].block_id, blocks[1].payload)
        ledger.speculate('GENESYS', blocks[2].block_id, blocks[1].payload)
        ledger.speculate('GENESYS', blocks[3].block_id, blocks[3].payload)
        ledger.speculate('0', blocks[4].block_id, blocks[1].payload)
        ledger.speculate('1', blocks[5].block_id, blocks[1].payload)
        ledger.commit('1')


    def test_commit_when_data_is_correct_return_Speculation_Tree_at_0(self):
        block_id = "Block_ID"
        speculation_tree = Ledger.commit(block_id)
        self.assertIsInstance(speculation_tree, SpeculationTree)

    def test_pending_state_when_data_is_correct_return_new_state(self):
        block_id = "Block_ID"
        speculation_tree = Ledger.commit(block_id)
        self.assertIsInstance(speculation_tree, SpeculationTree)


if __name__ == "__main__":
    unittest.main()
