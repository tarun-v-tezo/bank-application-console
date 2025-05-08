from models.Bank import Bank
from ..database import Database
from common.constants import DataKeys


class BankManager:
    __banks = []

    @classmethod
    def initialize(cls):
        cls.__banks = [Bank(**bankData) for bankData in Database.getData(DataKeys.BANKS)]

    @classmethod
    def getBanks(cls):
        return cls.__banks.copy()

    @classmethod
    def setBanks(cls, banks):
        cls.__banks = banks
        Database.setData(DataKeys.BANKS, cls.__banks)