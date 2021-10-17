from typing import List
from dataclasses import dataclass


@dataclass
class ValidatorInfo:
    author: int
    validator_pks: List[str]
    private_key: str
    client_pks: List[str]
    f: int  # f is upper bound on number of byzantine faults
