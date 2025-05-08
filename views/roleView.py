from common.constants import ActionNames, UserRoles
from services.AccountService import AccountService
from services.BankService import BankService
from services.CurrencyService import CurrencyService
from services.UsersService import UsersService
from util.helper import getActionChoiceForRole


class RoleView:
    def __init__(self):
        self.actionFunctionMapping = {
            ActionNames.CREATE_NEW_ACCOUNT: self.featureNotImplemented,
            ActionNames.EDIT_ACCOUNT: self.featureNotImplemented,
            ActionNames.DELETE_ACCOUNT: self.featureNotImplemented,
            ActionNames.ADD_NEW_ACCEPTED_CURRENCY: self.featureNotImplemented,
            ActionNames.VIEW_ACCOUNT_TRANSACTIONS: self.featureNotImplemented,
            ActionNames.REVERT_TRANSACTION: self.featureNotImplemented,
            ActionNames.ADD_SERVICE_CHARGE_SAME_BANK: self.featureNotImplemented,
            ActionNames.ADD_SERVICE_CHARGE_OTHER_BANK: self.featureNotImplemented,
            ActionNames.DEPOSIT_MONEY: self.featureNotImplemented,
            ActionNames.WITHDRAW_MONEY: self.featureNotImplemented,
            ActionNames.TRANSFER_MONEY: self.featureNotImplemented,
            ActionNames.VIEW_ACCOUNT_BALANCE: self.featureNotImplemented,
            ActionNames.VIEW_TRANSACTION_HISTORY: self.featureNotImplemented,
            ActionNames.ADD_NEW_USER: self.featureNotImplemented,
            ActionNames.REMOVE_USER: self.featureNotImplemented,
            ActionNames.ADD_NEW_BANK: self.featureNotImplemented,
            ActionNames.REMOVE_BANK: self.featureNotImplemented
        }
        self.usersService = UsersService()
        self.accountService = AccountService()
        self.bankService = BankService()
        self.currencyService = CurrencyService()
        self.glb_currentUser = UsersService.currentUser
        self.glb_currentBank = BankService.currentBank
    
    def featureNotImplemented(self):
        print("Feature not available! Please select another option.")

    def printInitialMessage(self, selectedAction):
        print("="*40)
        print(selectedAction['initialMessage'],"\n")

    def showMenu(self):
        while True:
            selectedAction = getActionChoiceForRole(UserRoles.EMPLOYEE)
            if not selectedAction:
                break
            assignedFunction = self.actionFunctionMapping.get(selectedAction['action'])
            self.printInitialMessage(selectedAction)
            assignedFunction()