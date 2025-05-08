from data.database import Database
from data.managers.acceptedCurrencyManager import AcceptedCurrencyManager
from data.managers.accountManager import AccountManager
from data.managers.bankManager import BankManager
from data.managers.roleManager import RoleManager
from data.managers.transactionManager import TransactionManager
from data.managers.userManager import UserManager
from data.managers.userRoleAssignmentManager import UserRoleAssignmentManager
from views.login import LoginView

def startup():
    # Initialize the database
    Database.initialize()
    AcceptedCurrencyManager.initialize()
    BankManager.initialize()
    AccountManager.initialize()
    UserManager.initialize()
    TransactionManager.initialize()
    RoleManager.initialize()
    UserRoleAssignmentManager.initialize()
    # print("Database initialized successfully.")

    # Call the index function
    loginView = LoginView()
    loginView.run()

if __name__ == "__main__":
    startup()