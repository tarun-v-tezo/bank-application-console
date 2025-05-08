from common.constants import ActionNames, Constants, UserRoles
from models.NewBankRequest import NewBankRequest
from models.NewUserRequest import NewUserRequest
from views.roleView import RoleView


class AdminView(RoleView):
    def __init__(self):
        super().__init__(UserRoles.ADMIN)
        self.actionFunctionMapping.update({
            ActionNames.ADD_NEW_USER: self.createUser,
            ActionNames.REMOVE_USER: self.removeUser,
            ActionNames.ADD_NEW_BANK: self.createBank,
            ActionNames.REMOVE_BANK: self.removeBank,
        })

    def createUser(self):

        username = input("Enter username: ")
        existingUser = self.usersService.getUser(username)
        if existingUser:
            print(f"A user with username '{username}' already exists. Please enter a different username.")

        password = input("Enter password: ")
        name = input("Enter name: ")
        role = None
        bankId = None
        while True:
            role = input("Enter role (admin/employee): ").lower()
            if role in ['admin', 'employee']:
                break
            else:
                print("Invalid role. Please enter 'admin' or 'employee'.")
        
        if role == 'admin':
            roleId = UserRoles.ADMIN
        elif role == 'employee':
            roleId = UserRoles.EMPLOYEE
            bankId = input("Enter bank Id: ")
            if not self.bank_service.getBankById(bankId):
                print(f"Bank with Id {bankId} not found.")
                return
            
        userRequest = NewUserRequest(
            username=username,
            password=password,
            name=name
        )

        newUser = self.usersService.createUserAndAssignRole(userRequest, roleId, bankId)
        if newUser:
            print(f"User {username} created successfully.")
        else:
            print("Failed to create user.")

    def removeUser(self):
        username = input("Enter username to delete: ")
        user = self.usersService.getUser(username)
        if user is None:
            print(f"User with username {username} not found.")
            return
        if user:
            self.usersService.removeUser(username)
            print(f"User {username} deleted successfully.")
        else:
            print(f"User {username} not found.")

    def createBank(self):
        bankName = input("Enter bank name: ")
        existingBank = self.bankService.getBankByName(bankName)
        if existingBank:
            print(f"A bank with name '{bankName}' already exists. Please enter a different name.")
            return

        newBankRequest = NewBankRequest(
            name=bankName
        )

        newBank = self.bankService.addBank(newBankRequest)
        if newBank:
            print(f"Bank {bankName} created successfully.")
        else:
            print("Failed to create bank.")
    
    def removeBank(self):
        bankName = input("Enter bank name: ")
        existingBank = self.bankService.getBankByName(bankName)
        if not existingBank:
            print(f"A bank with name '{bankName}' does not exist. Please enter a different name.")
            return
        resp = self.bankService.removeBank(bankName)
        if resp:
            print(f"Bank {bankName} deleted successfully.")
        else:
            print(f"Bank {bankName} deletion failed.")
        while True:
            print("\n" + "-" * 50)
            print("For exiting the application, type 'exit'")
            choice = input(Constants.AdminMainMenu)
            if choice == '1':
                print("Creating new user...")
                self.createUser()
            elif choice == '2':
                print("Deleting user...")
                self.deleteUser()
            elif choice == '3':
                print("Adding new bank...")
                # Implement add new bank functionality here
            elif choice == '4':
                print("Deleting bank...")
                # Implement delete bank functionality here
            elif choice.lower() == 'exit':
                print("Exiting the application.")
                break
            else:
                print("Invalid choice. Please try again.")
