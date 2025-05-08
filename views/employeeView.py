from common.constants import ActionNames, UserRoles
from models.NewAccountRequest import NewAccountRequest
from models.NewCurrencyRequest import NewCurrencyRequest
from models.NewUserRequest import NewUserRequest
from models.UpdateChargeRequest import UpdateChargeRequest
from .roleView import RoleView

class EmployeeView(RoleView):
    def __init__(self):
        super().__init__(UserRoles.EMPLOYEE)
        self.actionFunctionMapping.update({
            ActionNames.CREATE_NEW_ACCOUNT: self.createAccount,
            ActionNames.EDIT_ACCOUNT: self.editAccount,
            ActionNames.DELETE_ACCOUNT: self.deleteAccount,
            ActionNames.ADD_NEW_ACCEPTED_CURRENCY: self.addAcceptedCurrency,
            ActionNames.VIEW_ACCOUNT_TRANSACTIONS: self.viewAccountTransactions,
            ActionNames.REVERT_TRANSACTION: self.revertTransaction,
            ActionNames.ADD_SERVICE_CHARGE_SAME_BANK: self.addServiceChargeSameBank,
            ActionNames.ADD_SERVICE_CHARGE_OTHER_BANK: self.featureNotImplemented,
        })
        
    def checkBankAssociation(self):
        if self.glb_currentBank is None or self.glb_currentBank.id is None:
            print("You are not associated with any bank.")
            return False
        return True

    def createAccount(self):
        checkBankAssociation = self.checkBankAssociation()
        if not checkBankAssociation:
            return
        # Step 1: Ask for username and validate
        while True:
            username = input("Enter username: ")
            existingUser = self.usersService.getUser(username)

            if existingUser:
                print(f"A user with username '{username}' already exists.")
                useExisting = input("Do you want to use this user? (yes/no): ").strip().lower()
                if useExisting == 'yes':
                    customerId = existingUser.id
                    print(f"Using existing user with ID: {customerId}")
                    break
                else:
                    print("Please enter a different username.")
            else:
                # print(f"No user found with username '{username}'. Creating a new user.")
                # Step 2: Ask for user details and create a new user
                requiredUserDetails = {
                    "password": "Enter password: ",
                    "name": "Enter name: ",
                }

                userDetails = {"username": username}
                for key, prompt in requiredUserDetails.items():
                    userDetails[key] = input(prompt)

                # Create the new user
                userRequest = NewUserRequest(**userDetails)
                newUser = self.usersService.createUser(userRequest)
                if newUser is None:
                    print("Failed to create user. Please try again.")
                    return
                customerId = newUser.id
                print(f"New user created with ID: {customerId}")
                break

        # Step 3: Ask for account details
        bankId = self.glb_currentBank.id if self.glb_currentBank is not None else None
        
        requiredAccountDetails = {
            "accountType": "Enter account type: ",
            "initialDeposit": "Enter initial deposit amount: ",
        }

        accountDetails = {"customerId": customerId}
        for key, prompt in requiredAccountDetails.items():
            value = input(prompt)
            accountDetails[key] = value
        accountDetails["bankId"] = bankId
        accountDetails["initialDeposit"] = float(accountDetails["initialDeposit"]) if accountDetails["initialDeposit"] else 0.0

        # Step 4: Create the account
        resp = self.accountService.createBankAccount(NewAccountRequest(**accountDetails))
        print(resp)

    def editAccount(self):
        accountNumber = input("Enter account number to edit: ")
        editableFields = {
            "accountType": "Enter new account type: ",
        }
        account = self.accountService.getBankAccount(accountNumber)
        if account is None:
            print(f"Account with number {accountNumber} not found.")
            return
        newDetails = {}
        for field, prompt in editableFields.items():
            newValue = input(prompt)
            if newValue:
                newDetails[field] = newValue
        resp = self.accountService.updateBankAccount(accountNumber, newDetails)
        print(resp)
        
    def deleteAccount(self):
        accountNumber = input("Enter account number to delete: ")
        resp = self.accountService.deleteBankAccount(accountNumber)
        print(resp)
    
    def viewAccountTransactions(self):
        accountNumber = input("Enter account number to view transactions: ")
        transactions = self.accountService.getAccountTransactions(accountNumber)
        if transactions:
            print(f"\nTransactions for account {accountNumber}:")
            print("-" * 80)
            print(f"{'Transaction ID':<15} {'Amount':<10} {'Currency':<10} {'Type':<15} {'Date':<20} {'Status':<10}")
            print("-" * 80)
            for transaction in transactions:
                print(f"{transaction.id:<15} {transaction.amount:<10.2f} {transaction.currency:<10} {transaction.transactionType:<15} {transaction.transactionDate:<20} {transaction.status:<10}")
            print("-" * 80)
        else:
            print(f"No transactions found for account {accountNumber}.")
    
    def addAcceptedCurrency(self):
        checkBankAssociation = self.checkBankAssociation()
        if not checkBankAssociation:
            return
        bankId = self.glb_currentBank.id
        useExisting = 'no'
        currencyCode = None
        while True:
            currencyCode = input("Enter currency code: ")
            # Check if the currency code already exists
            existingCurrency = self.currencyService.getAcceptedCurrencyByCode(currencyCode)
            if existingCurrency:
                print(f"Currency code '{currencyCode}' already exists.")
                useExisting = input("Do you want to use this currency? (yes/no): ").strip().lower()
                if useExisting == 'yes':
                    acceptedCurrency = existingCurrency
                    print(f"Using existing currency: {acceptedCurrency}")
                    # Add the existing currency to the bank
                    resp = self.bankService.addExistingAcceptedCurrencyToBank(bankId, currencyCode)
                    if resp is None:
                        print("Failed to add existing accepted currency. Please try again.")
                        return
                    print(f"Existing accepted currency added to bank with code: {currencyCode}")
                    return
                else:
                    print("Please enter a different currency code.")
            else:
                useExisting = 'no'
                break
        if useExisting == 'no':
            # Step 2: Ask for currency details and create a new currency
            requiredCurrencyDetails = {
                "currencyName": "Enter currency name: ",
                "symbol": "Enter currency symbol: ",
                "exchangeRate": "Enter exchange rate: ",
            }

            currencyDetails = {"currencyCode": currencyCode}
            for key, prompt in requiredCurrencyDetails.items():
                value = input(prompt)
                currencyDetails[key] = value
            currencyDetails["exchangeRate"] = float(currencyDetails["exchangeRate"]) if currencyDetails["exchangeRate"] else 0.0
            resp = self.bankService.addNewAcceptedCurrencyToBank(bankId, NewCurrencyRequest(**currencyDetails))
            if resp is None:
                print("Failed to add new accepted currency. Please try again.")
                return
            print(f"New accepted currency created with code: {currencyCode}")
    
    def revertTransaction(self):
        transactionId = input("Enter transaction ID to revert: ")
        resp = self.accountService.revertTransaction(transactionId)
        print(resp)

    def addServiceChargeSameBank(self):
        checkBankAssociation = self.checkBankAssociation()
        if not checkBankAssociation:
            return
        bankId = self.glb_currentBank.id
        
        print("Current service charges:")
        print(f"RTGS: {self.glb_currentBank.rtgs}")
        print(f"IMPS: {self.glb_currentBank.imps}")
        
        requiredDetails = {
            "rtgs": "Enter new RTGS service charge: ",
            "imps": "Enter new IMPS service charge: ",
        }
        serviceCharges = {}
        for key, prompt in requiredDetails.items():
            while True:
                value = input(prompt)
                serviceCharges[key] = float(value) if value else None
                
                if serviceCharges[key] < 0:
                    print(f"Service charge for {key} cannot be negative.")
                else:
                    break
        updateChargeRequest = UpdateChargeRequest(
            bankId=bankId,
            **serviceCharges
        )
        resp = self.bankService.updateServiceCharges(updateChargeRequest)
        print(resp)

    def addServiceChargeOtherBank(self):
        checkBankAssociation = self.checkBankAssociation()
        if not checkBankAssociation:
            return
        bankId = self.glb_currentBank.id
        
        print("Current service charges:")
        print(f"RTGS: {self.glb_currentBank.ortgs}")
        print(f"IMPS: {self.glb_currentBank.oimps}")
        
        requiredDetails = {
            "ortgs": "Enter new RTGS service charge: ",
            "oimps": "Enter new IMPS service charge: ",
        }
        serviceCharges = {}
        for key, prompt in requiredDetails.items():
            while True:
                value = input(prompt)
                serviceCharges[key] = float(value) if value else None
                
                if serviceCharges[key] < 0:
                    print(f"Service charge for {key} cannot be negative.")
                else:
                    break
            
        updateChargeRequest = UpdateChargeRequest(
            bankId=bankId,
            **serviceCharges
        )
        resp = self.bankService.updateServiceCharges(updateChargeRequest)
        print(resp)