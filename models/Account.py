from dataclasses import dataclass


@dataclass
class Account:
    id: str
    customerId: int
    bankId: str
    accountType: str
    balance: float