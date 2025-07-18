from dataclasses import dataclass

@dataclass
class Wallet:
    user_id    : int
    address    : str
    private_key: str