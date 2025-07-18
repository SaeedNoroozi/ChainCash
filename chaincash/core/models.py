from dataclasses import dataclass

@dataclass
class Wallet:
    user_id    : int
    address    : str
    private_key: str

@dataclass
class DepositEvent:
    user_id: str | int
    token  : str
    amount : float
    tx_hash: str

@dataclass
class TransferResult:
    to_address: str
    token     : str
    amount    : float
    tx_hash   : str