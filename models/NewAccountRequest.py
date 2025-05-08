from dataclasses import dataclass
# from typing import Protocol

@dataclass
class NewAccountRequest:
    customerId: int # user id
    bankId: str
    accountType: str
    initialDeposit: float
