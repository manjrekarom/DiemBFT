from dataclasses import dataclass


@dataclass
class ValidatorInfo:
    author: int
    public_key: str
    private_key: str
    client_public_key: str
    f: int  # f is upper bound on number of byzantine faults
