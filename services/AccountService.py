from datetime import datetime
from common.constants import TransactionType, UserRoles
from data.managers.accountManager import AccountManager
from data.managers.transactionManager import TransactionManager
from models.Account import Account
from models.EditAccountRequest import EditAccountRequest
from models.NewAccountRequest import NewAccountRequest
from models.NewTransactionRequest import NewTransactionRequest
from models.Transaction import Transaction
from .BankService import BankService
from .UsersService import UsersService

class AccountService:
    def __init__(self):
        self.usersService = UsersService()
        self.bankService = BankService()
        self.bankAccounts = AccountManager.getBankAccounts()
        self.transactions = TransactionManager.getTransactions()

    def getBankAccount(self, accountId: str):
        for account in self.bankAccounts:
            if account.id == accountId:
                return account
        return None
    
    def getBankAccountByUserId(self, customerId: str, bankId: str):
        for account in self.bankAccounts:
            if account.customerId == customerId and account.bankId == bankId:
                return account
        return None

    def getBankAccountsByUser(self, userId: str):
        userAccounts = []
        for account in self.bankAccounts:
            if account.customerId == userId:
                userAccounts.append(account)
        return userAccounts
    
    def createBankAccount(self, accountDetails: NewAccountRequest):
        # Check if an account already exists for the given customerId and bankId
        for account in self.bankAccounts:
            if account.customerId == accountDetails.customerId and account.bankId == accountDetails.bankId:
                print(f"An account already exists for customer ID: {accountDetails.customerId} in bank ID: {accountDetails.bankId}.")
                return None
        
        # Validate customer
        customer = self.usersService.getUserById(accountDetails.customerId)
        if not customer:
            print("Customer ID not found in account details.")
            return None

        # Validate bank
        bank = self.bankService.getBankById(accountDetails.bankId)
        if not bank:
            print("Bank ID not found in account details.")
            return None

        # Create a new account object
        newAccount = Account(
            id=f"{customer.name[:3]}{datetime.now().strftime('%Y%m%d')}",
            customerId=customer.id,
            bankId=accountDetails.bankId,
            accountType=accountDetails.accountType,
            balance=0.0
        )

        # Add the new account to the bankAccounts list
        self.bankAccounts.append(newAccount)
        AccountManager.setBankAccounts(self.bankAccounts)

        if accountDetails.initialDeposit > 0:
            # Create a new transaction for the initial deposit
            initialDepositTransaction = NewTransactionRequest(
                amount=accountDetails.initialDeposit,
                transactionType=TransactionType.DEPOSIT,
                currency=bank.acceptedCurrencyIds[0],  # Assuming the first accepted currency is used
                fromAccountId=newAccount.id,
                toAccountId=newAccount.id,
                fromBankId=newAccount.bankId,
                toBankId=newAccount.bankId
            )
            transaction = self.makeTransaction(initialDepositTransaction)
            if not transaction:
                print("Failed to create initial deposit transaction.")
        
        # Add new role assignment for the user
        self.usersService.addUserRoleAssignment(customer.id, UserRoles.ACCOUNT_HOLDER, accountDetails.bankId)

        print(f"Account created successfully for customer ID: {customer.id} in bank ID: {accountDetails.bankId}.")
        return newAccount
    
    def updateBankAccount(self, accountNumber: str, newDetails: EditAccountRequest):
        # Find the account by account number
        for account in self.bankAccounts:
            if account.id == accountNumber:
                # Update the account details
                for key, value in newDetails.items():
                    setattr(account, key, value)
                AccountManager.setBankAccounts(self.bankAccounts)
                print(f"Account {accountNumber} updated successfully.")
                return account
        print(f"Account {accountNumber} not found.")
        return None
    
    def deleteBankAccount(self, accountNumber: str):
        # Find the account by account number
        for account in self.bankAccounts:
            if account.id == accountNumber:
                # Remove the account from the list
                self.bankAccounts.remove(account)
                AccountManager.setBankAccounts(self.bankAccounts)
                print(f"Account {accountNumber} deleted successfully.")
                return True
        print(f"Account {accountNumber} not found.")
        return False
    
    def getAccountTransactions(self, accountNumber: str):
        # Find the account by account number
        for account in self.bankAccounts:
            if account.id == accountNumber:
                # Get transactions for the account
                accountTransactions = [transaction for transaction in self.transactions if transaction.accountId == accountNumber]
                return accountTransactions
        print(f"Account {accountNumber} not found.")
        return None
    
    def makeTransaction(self, transactionDetails: NewTransactionRequest):
        # Validate the transaction details
        if transactionDetails.transactionType not in TransactionType.__dict__.values():
            print("Invalid transaction type.")
            return None
        if transactionDetails.transactionType == TransactionType.TRANSFER:
            if transactionDetails.amount <= 0:
                print("Transfer amount must be greater than zero.")
                return None
            if not transactionDetails.toAccountId or not transactionDetails.fromAccountId:
                print("Both from and to account IDs are required for transfer transactions.")
                return None
            for account in self.bankAccounts:
                        if account.id == transactionDetails.fromAccountId:
                            account.balance -= transactionDetails.amount
                        elif account.id == transactionDetails.toAccountId:
                            account.balance += transactionDetails.amount
        
        elif transactionDetails.transactionType == TransactionType.WITHDRAW:
            if transactionDetails.amount <= 0:
                print("Withdrawal amount must be greater than zero.")
                return None
            if not transactionDetails.fromAccountId:
                print("From account ID is required for withdrawal transactions.")
                return None
            for account in self.bankAccounts:
                        if account.id == transactionDetails.fromAccountId:
                            account.balance -= transactionDetails.amount
        
        elif transactionDetails.transactionType == TransactionType.DEPOSIT:
            if transactionDetails.amount <= 0:
                print("Deposit amount must be greater than zero.")
                return None
            if not transactionDetails.toAccountId:
                print("To account ID is required for deposit transactions.")
                return None
            for account in self.bankAccounts:
                        if account.id == transactionDetails.toAccountId:
                            account.balance += transactionDetails.amount
            
        # Validate the account
        account = self.getBankAccount(transactionDetails.fromAccountId)
        if not account:
            print("Account ID not found in transaction details.")
            return None
        if transactionDetails.fromAccountId != transactionDetails.toAccountId:
            toAccount = self.getBankAccount(transactionDetails.toAccountId)
            if not toAccount :
                print("Account ID not found in transaction details.")
                return None

        # Create a new transaction object
        newTransaction = Transaction(
            id=f"TXN{transactionDetails.fromBankId[:min(len(transactionDetails.fromBankId),3)]}{account.id[:min(len(account.id),3)]}{datetime.now().strftime('%Y%m%d%H%M%S')}",
            accountId=transactionDetails.fromAccountId,
            amount=transactionDetails.amount,
            transactionType=transactionDetails.transactionType,
            currency=transactionDetails.currency,
            status="COMPLETED",
            transactionDate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            fromAccountId=transactionDetails.fromAccountId if transactionDetails.transactionType == "TRANSFER" else None,
            toAccountId=transactionDetails.toAccountId if transactionDetails.transactionType == "TRANSFER" else None,
            fromBankId=transactionDetails.fromBankId if transactionDetails.transactionType == "TRANSFER" else None,
            toBankId=transactionDetails.toBankId if transactionDetails.transactionType == "TRANSFER" else None,
            # Set the reverted fields to None for new transactions
            revertedDate=None,
            revertedBy=None,
            # Set the reverted flag to False for new transactions
            reverted=False
        )

        # Add the new transaction to the transactions list
        self.transactions.append(newTransaction)
        TransactionManager.setTransactions(self.transactions)

        print(f"Transaction {newTransaction.id} added successfully.")
        return newTransaction
    
    def revertTransaction(self, transactionId: str):
        # Find the transaction by transaction ID
        for transaction in self.transactions:
            if transaction.id == transactionId:
                if transaction.reverted:
                    print(f"Transaction {transactionId} has already been reverted.")
                    return False
                if transaction.transactionType == TransactionType.DEPOSIT:
                    # Revert deposit by subtracting the amount from the account balance
                    for account in self.bankAccounts:
                        if account.id == transaction.accountId:
                            account.balance -= transaction.amount
                            break
                elif transaction.transactionType == TransactionType.WITHDRAW:
                    # Revert withdrawal by adding the amount to the account balance
                    for account in self.bankAccounts:
                        if account.id == transaction.accountId:
                            account.balance += transaction.amount
                            break
                elif transaction.transactionType == TransactionType.TRANSFER:
                    # Revert transfer by adding the amount back to the sender's account and subtracting from the receiver's account
                    for account in self.bankAccounts:
                        if account.id == transaction.fromAccountId:
                            account.balance += transaction.amount
                        elif account.id == transaction.toAccountId:
                            account.balance -= transaction.amount
                
                # Mark the transaction as reverted
                transaction.reverted = True
                transaction.revertedDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                transaction.revertedBy = self.usersService.currentUser.id
                # Update the transaction in the list
                for i, t in enumerate(self.transactions):
                    if t.id == transactionId:
                        self.transactions[i] = transaction
                        break
                # Save the updated transactions list to the database
                TransactionManager.setTransactions(self.transactions)
                print(f"Transaction {transactionId} reverted successfully.")
                return True
        print(f"Transaction {transactionId} not found.")
        return False