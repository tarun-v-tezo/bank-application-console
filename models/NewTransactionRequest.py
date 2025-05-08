from dataclasses import dataclass


@dataclass
class NewTransactionRequest:
    fromAccountId: str
    toAccountId: str
    amount: float
    currency: str
    transactionType: str
    fromBankId: str
    toBankId: str
    