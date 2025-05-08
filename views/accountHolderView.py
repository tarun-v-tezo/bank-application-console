from common.constants import ActionNames, Constants, TransactionType, UserRoles
from models.NewTransactionRequest import NewTransactionRequest
from views.roleView import RoleView


class AccountHolderView(RoleView):
    def __init__(self):
        super().__init__(UserRoles.ACCOUNT_HOLDER)
        self.actionFunctionMapping.update({
            ActionNames.DEPOSIT_MONEY: self.depositMoney,
            ActionNames.WITHDRAW_MONEY: self.withdrawMoney,
            ActionNames.TRANSFER_MONEY: self.transferMoney(),
            ActionNames.VIEW_TRANSACTION_HISTORY: self.viewTransactionHistory()
        })
        self.glb_currentAccount = None
        self.__setCurrentAccount()
        
    
    def __setCurrentAccount(self):
        self.defaultCurrencyId = self.currencyService.getCurrencyIdByCode(Constants.DefaultCurrencyCode)
        self.glb_currentAccount = self.accountService.getBankAccountByUserId(self.glb_currentUser.id, self.glb_currentBank.id)
        if self.glb_currentAccount is None:
            print("No account found for the current user.")
            return


    def getTransactionDetails(self, amount: float = 0.0, transactionType: TransactionType = TransactionType.DEPOSIT, toAccountId: str = None, toBankId: str = None):
        transactionDetails = NewTransactionRequest(
            fromAccountId=self.glb_currentAccount.id,
            toAccountId=toAccountId if toAccountId else self.glb_currentAccount.id,
            amount=amount,
            currency=self.defaultCurrencyId,
            transactionType=transactionType,
            fromBankId=self.glb_currentBank.id,
            toBankId=toBankId if toBankId else self.glb_currentBank.id
        )
        return transactionDetails

    def depositMoney(self):
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("Invalid amount entered.")
            return
        if amount > Constants.MaxDepositAmount:
            print(f"Maximum deposit amount is {Constants.MaxDepositAmount} {Constants.DefaultCurrencyCode}.")
            return
        if amount < Constants.MinDepositAmount:
            print(f"Minimum deposit amount is {Constants.MinDepositAmount} {Constants.DefaultCurrencyCode}.")
            return
        currencyCode = input("Enter currency code: ")
        if not self.bankService.isCurrencyAcceptedByBank(self.glb_currentBank.id, currencyCode):
            print(f"Currency {currencyCode} is not accepted by bank {self.glb_currentBank.name}.")
            return
        currency = self.currencyService.getAcceptedCurrencyByCode(currencyCode)
        if currency is None:
            print(f"Currency with code {currencyCode} not found.")
            return
        if currency.id != self.defaultCurrencyId:
            convertedAmount = self.currencyService.convertCurrency(amount, currency.id, self.defaultCurrencyId)
            if convertedAmount is None:
                print("Failed to convert currency.")
                return
            print(f"Converted amount: {convertedAmount} {self.currencyService.getAcceptedCurrencyById(self.defaultCurrencyId).currencyCode}")
            amount = convertedAmount
        transactionDetails = self.getTransactionDetails(amount, TransactionType.DEPOSIT)
        
        if self.accountService.makeTransaction(transactionDetails):
            print(f"Deposited {amount} to account {self.glb_currentAccount.id}.")
        else:
            print("Failed to deposit money.")
    
    def withdrawMoney(self):
        if self.glb_currentAccount.balance <= Constants.MinBalance:
            print(f"Minimum balance should be maintained: {Constants.MinBalance} {Constants.DefaultCurrencyCode}.")
            return
        if self.glb_currentAccount.balance < Constants.MinWithdrawAmount:
            print(f"Insufficient balance to withdraw {Constants.MinWithdrawAmount} {Constants.DefaultCurrencyCode}.")
            return
        
        # only default currency is allowed to withdraw
        amount = float(input(f"Enter amount to withdraw ({Constants.DefaultCurrencyCode}): "))
        if amount <= 0:
            print("Invalid amount entered.")
            return
        if amount > self.glb_currentAccount.balance:
            print(f"Insufficient balance to withdraw {amount} {Constants.DefaultCurrencyCode}.")
            return
        if amount < Constants.MinWithdrawAmount:
            print(f"Minimum withdrawal amount is {Constants.MinWithdrawAmount} {Constants.DefaultCurrencyCode}.")
            return
        if amount > self.glb_currentAccount.balance - Constants.MinBalance:
            print(f"Cannot withdraw more than {self.glb_currentAccount.balance - Constants.MinBalance} {Constants.DefaultCurrencyCode}.")
            return
        if amount > Constants.MaxWithdrawAmount:
            print(f"Maximum withdrawal amount is {Constants.MaxWithdrawAmount} {Constants.DefaultCurrencyCode}.")
            return
        transactionDetails = self.getTransactionDetails(amount, TransactionType.WITHDRAW)

        if self.accountService.makeTransaction(transactionDetails):
            print(f"Withdrew {amount} from account {self.glb_currentAccount.id}.")
        else:
            print("Failed to withdraw money.")
            
    def transferMoney(self):
        if self.glb_currentAccount.balance <= Constants.MinBalance:
            print(f"Minimum balance should be maintained: {Constants.MinBalance} {Constants.DefaultCurrencyCode}.")
            return
        if self.glb_currentAccount.balance < Constants.MinTransferAmount:
            print(f"Insufficient balance to transfer {Constants.MinTransferAmount} {Constants.DefaultCurrencyCode}.")
            return
        recipientAccountId = input("Enter recipient account ID: ")
        recipientAccount = self.accountService.getBankAccount(recipientAccountId)
        if recipientAccount is None:
            print(f"Recipient account with ID {recipientAccountId} not found.")
            return
        amount = float(input("Enter amount to transfer: "))
        if amount <= 0:
            print("Invalid amount entered.")
            return
        if amount > self.glb_currentAccount.balance:
            print(f"Insufficient balance to transfer {amount} {Constants.DefaultCurrencyCode}.")
            return
        if amount < Constants.MinTransferAmount:
            print(f"Minimum transfer amount is {Constants.MinTransferAmount} {Constants.DefaultCurrencyCode}.")
            return
        if amount > self.glb_currentAccount.balance - Constants.MinBalance:
            print(f"Cannot transfer more than {self.glb_currentAccount.balance - Constants.MinBalance} {Constants.DefaultCurrencyCode}.")
            return
        if amount > Constants.MaxTransferAmount:
            print(f"Maximum transfer amount is {Constants.MaxTransferAmount} {Constants.DefaultCurrencyCode}.")
            return
        transactionDetails = self.getTransactionDetails(amount, TransactionType.TRANSFER, recipientAccountId, recipientAccount.bankId)
        if self.accountService.makeTransaction(transactionDetails):
            print(f"Transferred {amount} to account {recipientAccountId}.")
        else:
            print("Failed to transfer money.")
    
    def viewTransactionHistory(self):
        accountNumber = self.glb_currentAccount.id
        if not accountNumber:
            print("No account number found.")
            return
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
    
    def showMenu(self):
        while True:
            print("\n" + "-" * 50)
            print("For exiting the application, type 'exit'")
            choice = input(Constants.AccountHolderMainMenu)

            if choice == '1':
                print("Deposit Money")
                self.depositMoney()
            elif choice == '2':
                print("Withdraw Money")
                self.withdrawMoney()
            elif choice == '3':
                print("Transfer Money")
                self.transferMoney()
            elif choice == '4':
                print("View Transaction History")
                self.viewTransactionHistory()
            elif choice.lower() == 'exit':
                print("Exiting the application.")
                break
            else:
                print("Invalid choice. Please try again.")
            
    