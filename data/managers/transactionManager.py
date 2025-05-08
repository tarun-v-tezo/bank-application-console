from models.Transaction import Transaction
from ..database import Database
from common.constants import DataKeys


class TransactionManager:
    __transactions = []

    @classmethod
    def initialize(cls):
        cls.__transactions = [Transaction(**transactionData) for transactionData in Database.getData(DataKeys.TRANSACTIONS)]

    @classmethod
    def getTransactions(cls):
        return cls.__transactions.copy()

    @classmethod
    def setTransactions(cls, transactions):
        cls.__transactions = transactions
        Database.setData(DataKeys.TRANSACTIONS, cls.__transactions)