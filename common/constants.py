from enum import Enum


class DataKeys:
    BANKS = "banks"
    BANK_ACCOUNTS = "bank_accounts"
    USERS = "users"
    TRANSACTIONS = "transactions"
    ROLES = "roles"
    USERROLEASSIGNMENTS = "user_role_assignments"
    ACCEPTEDCURRENCIES = "accepted_currencies"

class TransactionType:
    DEPOSIT = 1
    WITHDRAW = 2
    TRANSFER = 3
    REVERT = 4

class UserRoles:
    EMPLOYEE = 1
    ACCOUNT_HOLDER = 2
    ADMIN = 3

class ActionNames(Enum):
    # Employee Actions
    CREATE_NEW_ACCOUNT = "EA001"
    EDIT_ACCOUNT = "EA002"
    DELETE_ACCOUNT = "EA003"
    ADD_NEW_ACCEPTED_CURRENCY = "EA004"
    VIEW_ACCOUNT_TRANSACTIONS = "EA005"
    REVERT_TRANSACTION = "EA006"
    ADD_SERVICE_CHARGE_SAME_BANK = "EA007"
    ADD_SERVICE_CHARGE_OTHER_BANK = "EA008"

    # Account Holder Actions
    DEPOSIT_MONEY = "HA001"
    WITHDRAW_MONEY = "HA002"
    TRANSFER_MONEY = "HA003"
    VIEW_ACCOUNT_BALANCE = "HA004"
    VIEW_TRANSACTION_HISTORY = "HA005"

    # Admin Actions
    ADD_NEW_USER = "AA001"
    REMOVE_USER = "AA002"
    ADD_NEW_BANK = "AA003"
    REMOVE_BANK = "AA004"

class Constants:
    DefaultCurrencyCode = "INR"
    MinBalance = 1000.0
    MinWithdrawAmount = 100.0
    MinTransferAmount = 100.0
    MaxTransferAmount = 100000.0
    MaxWithdrawAmount = 50000.0
    MaxDepositAmount = 100000.0
    MinDepositAmount = 100.0
    EXIT_COMMAND = 'exit'
    RoleConfigurations = [
        {
            "roleName": "Employee",
            "roleId": UserRoles.EMPLOYEE,
            "actions": [
                {"action": ActionNames.CREATE_NEW_ACCOUNT, "title": "Create new account", "initialMessage": "Creating new account..."},
                {"action": ActionNames.EDIT_ACCOUNT, "title": "Edit account", "initialMessage": "Editing account..."},
                {"action": ActionNames.DELETE_ACCOUNT, "title": "Delete account", "initialMessage": "Deleting account..."},
                {"action": ActionNames.ADD_NEW_ACCEPTED_CURRENCY, "title": "Add new Accepted Currency", "initialMessage": "Adding accepted currency..."},
                {"action": ActionNames.VIEW_ACCOUNT_TRANSACTIONS, "title": "View account transactions", "initialMessage": "Viewing account transactions..."},
                {"action": ActionNames.REVERT_TRANSACTION, "title": "Revert transaction", "initialMessage": "Reverting transaction..."},
                {"action": ActionNames.ADD_SERVICE_CHARGE_SAME_BANK, "title": "Add service charge to same bank", "initialMessage": "Adding service charge to same bank..."},
                {"action": ActionNames.ADD_SERVICE_CHARGE_OTHER_BANK, "title": "Add service charge to other bank", "initialMessage": "Adding service charge to other bank..."},
            ]
        },
        {
            "roleName": "Account Holder",
            "roleId": UserRoles.ACCOUNT_HOLDER,
            "actions": [
                {"action": ActionNames.DEPOSIT_MONEY, "title": "Deposit money", "initialMessage": "Depositing money..."},
                {"action": ActionNames.WITHDRAW_MONEY, "title": "Withdraw money", "initialMessage": "Withdrawing money..."},
                {"action": ActionNames.TRANSFER_MONEY, "title": "Transfer money", "initialMessage": "Transfering money..."},
                {"action": ActionNames.VIEW_ACCOUNT_BALANCE, "title": "View account balance", "initialMessage": "Viewing account balance..."},
                {"action": ActionNames.VIEW_TRANSACTION_HISTORY, "title": "View transaction history", "initialMessage": "Viewing transactions..."},
            ]
        },
        {
            "roleName": "Account Holder",
            "roleId": UserRoles.ACCOUNT_HOLDER,
            "actions": [
                {"action": ActionNames.ADD_NEW_USER, "title": "Add a new user", "initialMessage": "Adding new user..."},
                {"action": ActionNames.REMOVE_USER, "title": "Remove a user", "initialMessage": "Removing user..."},
                {"action": ActionNames.ADD_NEW_BANK, "title": "Add a new bank", "initialMessage": "Adding new bank..."},
                {"action": ActionNames.REMOVE_BANK, "title": "Remove a bank", "initialMessage": "Removing bank..."},
            ]
        }
    ]