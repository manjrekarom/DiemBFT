from typing import Dict, List, Set
from dataclasses import dataclass
from collections import defaultdict, deque

from info import ValidatorInfo
from crypto import hasher, sign
from src.ledger import NoopTxnEngine


@dataclass
class VoteInfo:
    block_id: str
    round: int
    parent_block_id: str
    parent_round: int
    exec_state_id: str

    def to_tuple(self):
        return (self.block_id, self.round, self.parent_block_id, 
        self.parent_round, self.exec_state_id)


@dataclass
class LedgerCommitInfo:
    commit_state_id: int
    vote_info_hash: str

    def from_tuple(commit_state_id, vote_info_hash):
        return LedgerCommitInfo(commit_state_id, vote_info_hash)

    def to_tuple(self):
        return (self.commit_state_id, self.vote_info_hash)


@dataclass
class QC:
    vote_info: VoteInfo
    ledger_commit_info: LedgerCommitInfo
    signatures: Set[str]
    author: int
    author_signature: str

    def from_tuple(vote_info, ledger_commit_info, signatures, author, 
    author_signature):
        vote_info = VoteInfo(*vote_info)
        ledger_commit_info = LedgerCommitInfo(*ledger_commit_info)
        return QC(vote_info, ledger_commit_info, signatures, author, author_signature)

    def to_tuple(self):
        return ('QC', self.vote_info.to_tuple(), self.ledger_commit_info.to_tuple(), 
        self.signatures, self.author, self.author_signature)


@dataclass
class VoteMsg:
    vote_info: VoteInfo
    ledger_commit_info: LedgerCommitInfo
    high_commit_qc: QC
    sender: str  # added automatically when constructed
    # TODO: signature types
    signature: str  # signed automatically when constructed

    @staticmethod
    def from_tuple(vote_info, ledger_commit_info, high_commit_qc, sender, signature):
        vote_info = VoteInfo.from_tuple(vote_info)
        ledger_commit_info = LedgerCommitInfo.from_tuple(ledger_commit_info)
        qc = QC.from_tuple(high_commit_qc)
        return VoteMsg(vote_info, ledger_commit_info, qc, sender, signature)

    def to_tuple(self):
        return ('VoteMsg', self.vote_info.to_tuple(), self.ledger_commit_info.to_tuple, self.high_commit_qc.to_tuple(), self.sender, self.signature)


@dataclass
class Block:
    author: int
    round: int
    payload: str
    qc: QC
    block_id: str

    def to_tuple(self):
        return (self.author, self.round, self.payload, self.qc.to_tuple(), self.block_id)    


@dataclass
class PendingBlock:
    """
    Wrapper over Block. Contains additional references
    """
    block: Block
    vote_info: VoteInfo
    parent: 'PendingBlock'
    children: List['PendingBlock'] = None


class PendingBlockTree:
    _root: PendingBlock
    _ids_to_block: Dict[str, PendingBlock]

    def __init__(self, root=None) -> None:
        # create genesys block
        if not root:
            # genesys
            b_id = hasher(99999999, 0, 'GENESYS', '', '')
            vote_info = VoteInfo(b_id, 0, None, None, NoopTxnEngine.execute_transactions(None, b_id, 'GENESYS'))
            b = Block(99999999, 0, 'GENESYS', None, b_id)
            root = PendingBlock(b, vote_info, None, []) # Meaning of life, 
            # universe and everything
        assert root.parent == None
        self._root: PendingBlock = root
        self._ids_to_state: Dict[str, PendingBlock] = {}
        self._ids_to_state = self.make_ids_to_state_from_root(root)

    def get_state_by_block_id(self, block_id):
        return self._ids_to_state[block_id]

    def make_ids_to_state_from_root(self, root):
        # bfs on root
        dq = deque([root])
        hm = {}
        while len(dq):
            node = dq.popleft()
            hm[node.block.block_id] = node
            if node.children:
                dq.extend(node.children)
        return hm

    def prune(self, block_id):
        node = self.get_state_by_block_id(block_id)
        nodes_pending_commit = []
        while node.parent != None:
            nodes_pending_commit.append(node)
            node = node.parent
        nodes_pending_commit = nodes_pending_commit[::-1]
        # TODO: Write nodes to file
        # self._ledger.writelines(list(map(str, nodes_pending_commit)))
        with open(self._ledger_file_name, 'a+') as f:
            f.writelines(list(map(str, nodes_pending_commit)))
        # print(self._ledger)
        # prune other branches
        new_root = nodes_pending_commit[0]
        new_root.parent = None
        self._speculation_tree = PendingBlockTree(nodes_pending_commit[0])
        # return self._speculation_tree

    def add(self, block: Block):
        parent_block_id = block.qc.vote_info.block_id
        assert self._ids_to_block[block.qc.vote_info.block_id] != None
        parent_block = self._ids_to_state[parent_block_id]
        if not parent_block.children:
            parent_block.children = []
        parent_block.children.append(block)
        block.parent = parent_block


class BlockTree:
    pending_block_tree: PendingBlockTree
    ledger: 'Ledger'
    # TODO: Initialize
    high_commit_qc: QC
    high_qc: QC = 0
    pending_votes: defaultdict
    validator_info: ValidatorInfo

    def __init__(self, ledger: 'Ledger', validator_info: 'ValidatorInfo') -> None:
        # TODO: Initialize better
        self.ledger = ledger
        self.validator_info = validator_info
        self.pending_block_tree = PendingBlockTree()
        self.pending_votes = defaultdict(set)

    def process_qc(self, qc: QC):
        """
        process_qc is used to commit a state to ledger. It is called when 
        a proposal or timeout message or a vote comes.
        """
        if qc.ledger_commit_info.commit_state_id != None:
            self.ledger.commit(qc.vote_info.parent_block_id)
            self.pending_block_tree.prune(qc.vote_info.parent_block_id)
            # high_commit_qc = max_round(qc, high_commit_qc)
            if qc.vote_info.round > self.high_commit_qc.vote_info.round:
                self.high_commit_qc = qc
        # high_qc = max_round(qc, high_qc)
        if qc.vote_info.round > self.high_qc.vote_info.round:
            self.high_qc = qc

    def execute_and_insert(self, block: Block):
        self.ledger.speculate(block.qc.vote_info.block_id, block.block_id, 
        block.payload)
        self.pending_block_tree.add(block)

    def process_vote(self, vote_msg: VoteMsg):
        self.process_qc(vote_msg.high_commit_qc)
        # TODO: replace with cryptographic hash
        vote_idx = hasher(vote_msg.ledger_commit_info)
        self.pending_votes[vote_idx].add(vote_msg.signature)
        if len(self.pending_votes[vote_idx]) == 2 * f + 1:
            signatures = self.pending_votes[vote_idx]
            qc = QC(vote_info=vote_msg.vote_info, 
                ledger_commit_info=vote_msg.ledger_commit_info.commit_state_id, 
                signatures=self.pending_votes[vote_idx], 
                author=self.validator_info.author, 
                author_signature=sign(signatures, self.validator_info.private_key))
            return qc
        return None

    def generate_block(self, txns, current_round):
        # TODO: check below statement
        h = hasher(self.validator_info.author, current_round, txns, self.high_qc.vote_info.block_id, self.high_qc.signatures)
        return Block(author=self.validator_info.author, round=current_round, 
        payload=txns, qc=self.high_qc, block_id=h)
