from dataclasses import dataclass


@dataclass
class Block:
    author: str
    round: int
    payload: str
    qc: 'QC'
    block_id: str
