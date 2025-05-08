from models.Account import Account
from ..database import Database
from common.constants import DataKeys


class AccountManager:
    __bankAccounts = []

    @classmethod
    def initialize(cls):
        cls.__bankAccounts = [Account(**accountData) for accountData in Database.getData(DataKeys.BANK_ACCOUNTS)]

    @classmethod
    def getBankAccounts(cls):
        return cls.__bankAccounts.copy()

    @classmethod
    def setBankAccounts(cls, bankAccounts):
        cls.__bankAccounts = bankAccounts
        Database.setData(DataKeys.BANK_ACCOUNTS, cls.__bankAccounts)