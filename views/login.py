from common.constants import UserRoles
from services.BankService import BankService
from services.UsersService import UsersService
from views.accountHolderView import AccountHolderView
from views.adminView import AdminView
from .employeeView import EmployeeView


class LoginView:
    def __init__(self):
        self.usersService = UsersService()
        self.gbl_curUser = None

    def run(self):
        if not self.login():
            return

        selectedRoleWithBanks = self.selectUserRole()
        selectedRole = selectedRoleWithBanks["role"]
        associatedBankIds = selectedRoleWithBanks.get("bankIds", [])

        selectedBankId = self.selectBank(associatedBankIds)
        if selectedBankId:
            BankService.setCurrentBankById(selectedBankId)
            print(f"You are logged in as a {selectedRole.roleName} for Bank ID: {selectedBankId}.")
        else:
            print(f"You are logged in as a {selectedRole.roleName} with no associated banks.")

        self.showMenu(selectedRole, selectedBankId)

    def login(self):
        print("\n" + "=" * 40)
        print("Welcome to the Bank Management System")
        print("=" * 40)

        while True:
            username = input("\nEnter username (or type 'exit' to quit): ").strip()
            if username.lower() == 'exit':
                print("\nThank you for using the system. Goodbye!")
                print("=" * 40)
                return False

            password = input("Enter password: ").strip()
            if self.usersService.validateUser(username, password):
                self.gbl_curUser = self.usersService.currentUser
                print("\n" + "=" * 40)
                print(f"Hello, {self.gbl_curUser.name if self.gbl_curUser else 'Guest'}!")
                print("=" * 40)
                return True
            else:
                print("\nInvalid username or password. Please try again.")

    def selectUserRole(self):
        roles = self.usersService.getUserRoles(self.gbl_curUser.username)

        if not roles:
            print("No roles found for the user.")
            return None

        if len(roles) == 1:
            return roles[0]

        print("You have multiple roles. Please select one:")
        for idx, roleWithBanks in enumerate(roles):
            role = roleWithBanks["role"]
            bankIds = roleWithBanks.get("bankIds", [])
            bankInfo = f"(Banks: {', '.join(bankIds)})" if bankIds else "(No banks)"
            print(f"{idx + 1}. {role.roleName} {bankInfo}")

        selectedIndex = self.getValidIndexInput(len(roles), "Enter your choice: ")
        return roles[selectedIndex]

    def selectBank(self, bankIds):
        if not bankIds:
            return None

        if len(bankIds) == 1:
            return bankIds[0]

        print("This role is associated with multiple banks. Please select one:")
        for idx, bankId in enumerate(bankIds):
            print(f"{idx + 1}. Bank ID: {bankId}")

        selectedIndex = self.getValidIndexInput(len(bankIds), "Enter your choice: ")
        return bankIds[selectedIndex]

    def getValidIndexInput(self, limit, prompt):
        while True:
            try:
                choice = int(input(prompt).strip()) - 1
                if 0 <= choice < limit:
                    return choice
                print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def showMenu(self, role, bankId):
        print(f"\nAccessing {role.roleName} features" + (f" for Bank ID: {bankId}." if bankId else "."))

        if role.id == UserRoles.EMPLOYEE:
            EmployeeView().showMenu()
        elif role.id == UserRoles.ACCOUNT_HOLDER:
            AccountHolderView().showMenu()
        elif role.id == UserRoles.ADMIN:
            AdminView().showMenu()
        else:
            print("Unknown role. Access denied.")
