import json

from common.constants import DataKeys
from models.AcceptedCurrency import AcceptedCurrency
from models.Account import Account
from models.Bank import Bank
from models.Roles import Role
from models.Transaction import Transaction
from models.User import User
from models.UserRoleAssignment import UserRoleAssignment

class Database:
    __file_path = 'C:/Codes/Python/Bank Task/data/data.json'
    banks = list[Bank]()
    bankAccounts = list[Account]()
    users = list[User]()
    transactions = list[Transaction]()
    roles = list[Role]()
    userRoleAssignments = list[UserRoleAssignment]()
    acceptedCurrencies = list[AcceptedCurrency]()
    
    @classmethod
    def initialize(cls):
        cls.__data = cls.__loadData()
        cls.banks = [Bank(**bankData) for bankData in cls.__getData(DataKeys.BANKS)]
        cls.bankAccounts = [Account(**accountData) for accountData in cls.__getData(DataKeys.BANK_ACCOUNTS)]
        cls.users = [User(**user) for user in cls.__getData(DataKeys.USERS)]
        cls.transactions = [Transaction(**transaction) for transaction in cls.__getData(DataKeys.TRANSACTIONS)]
        cls.roles = [Role(**role) for role in cls.__getData(DataKeys.ROLES)]
        cls.userRoleAssignments = [UserRoleAssignment(**assignment) for assignment in cls.__getData(DataKeys.USERROLEASSIGNMENTS)]
        cls.acceptedCurrencies = [AcceptedCurrency(**currency) for currency in cls.__getData(DataKeys.ACCEPTEDCURRENCIES)]
    
    @classmethod
    def __loadData(cls):
        try:
            with open(cls.__file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            print("error")
            return {}

    @classmethod
    def __getData(cls, key: str):
        if key in cls.__data:
            return cls.__data[key]
        else:
            return []

    @classmethod
    def setData(cls, key: str, value):
        cls.__data[key] = [item.__dict__ for item in value]
        cls.__saveData()

    @classmethod
    def __saveData(cls):
        # cls.__data[DataKeys.BANKS] = [bank.__dict__ for bank in cls.banks]
        # cls.__data[DataKeys.BANK_ACCOUNTS] = [account.__dict__ for account in cls.bankAccounts]
        # cls.__data[DataKeys.USERS] = [user.__dict__ for user in cls.users]
        # cls.__data[DataKeys.TRANSACTIONS] = [transaction for transaction in cls.transactions]
        with open(cls.__file_path, 'w') as file:
            json.dump(cls.__data, file, indent=4)


