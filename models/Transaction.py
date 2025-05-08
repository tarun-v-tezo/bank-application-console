from dataclasses import dataclass
from typing import Optional


@dataclass
class Transaction:
    id: str
    accountId: str
    amount: float
    currency: str
    transactionType: str
    transactionDate: str
    status: str
    fromAccountId: str
    toAccountId: str
    fromBankId: str
    toBankId: str
    reverted: bool
    revertedDate: Optional[str] = None
    revertedBy: Optional[int] = None