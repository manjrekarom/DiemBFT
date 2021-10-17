from typing import Set
from dataclasses import dataclass

from block import QC, Block

@dataclass
class TimeoutInfo:
    round: int
    high_qc: QC
    sender: str  # should be automatically added when created
    # TODO: might need to change it to bytes
    signature: str  # sign_u(round, high_qc.round) // automatically signed
    # when constructed


@dataclass
class TC:
    round: int
    tmo_high_qc_rounds: Set[int]
    # TODO: signatures might change to bytes
    tmo_signatures: Set[str]


@dataclass
class TimeoutMsg:
    tmo_info: TimeoutInfo
    last_round_tc: TC
    high_commit_qc: QC


@dataclass
class ProposalMsg:
    block: Block
    last_round_tc: TC
    high_commit_qc: QC
    # TODO: might need to change to bytes
    signature: str
