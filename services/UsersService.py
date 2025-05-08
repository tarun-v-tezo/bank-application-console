from data.managers.roleManager import RoleManager
from data.managers.userManager import UserManager
from data.managers.userRoleAssignmentManager import UserRoleAssignmentManager
from models.NewUserRequest import NewUserRequest
from models.Roles import Role
from models.User import User
from models.UserRoleAssignment import UserRoleAssignment

class UsersService:
    currentUser: User = None
    def __init__(self):
        self.users = UserManager.getUsers()
        self.userRoleAssignments = UserRoleAssignmentManager.getUsers()
        self.roles = RoleManager.getRoles()

    def getUser(self, username: str):
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def getUserById(self, userId: int):
        for user in self.users:
            if user.id == userId:
                return user
        return None
    
    def createUserAndAssignRole(self, userRequest: NewUserRequest, roleId: int, bankId: str = None):
        user = self.createUser(userRequest)
        if user is None:
            return None
        self.addUserRoleAssignment(user.id, roleId, bankId)
        return user
    
    def createUser(self, userRequest: NewUserRequest):
        user = User(
            id=len(self.users) + 1, # need to implement a better way to get the id
            name=userRequest.name,
            username=userRequest.username,
            password=userRequest.password
        )
        if self.getUser(user.username) is not None:
            print(f"User with username {user.username} already exists.")
            return None
        self.users.append(user)
        UserManager.setUsers(self.users)
        return user
    
    def validateUser(self, username: str, password: str) -> bool:
        for user in self.users:
            if user.username == username and user.password == password:
                self.setCurrentUser(user)
                return True
        return False
    
    @classmethod
    def setCurrentUser(cls, user: User):
        cls.currentUser = user
    
    def getUserRoles(self, username: str):
        userRoles:list[Role] = []
        for user in self.users:
            if user.username == username:
                userRoles = self.__getRolesWithBanksByUserId(user.id)
                break
        return userRoles
    
    def addUserRoleAssignment(self, userId: int, roleId: int, bankId: str = None):
        # Check if the user already has the role assigned
        for assignment in self.userRoleAssignments:
            if assignment.userId == userId and assignment.roleId == roleId:
                print(f"User {userId} already has role {roleId} assigned.")
                return False
        
        # Create a new role assignment
        newAssignment = UserRoleAssignment(
            id=len(self.userRoleAssignments) + 1,  # need to implement a better way to get the id
            userId=userId,
            roleId=roleId,
            bankId=bankId
        )
        self.userRoleAssignments.append(newAssignment)
        UserRoleAssignmentManager.setUsers(self.userRoleAssignments)
        return True
    
    def __getRolesWithBanksByUserId(self, userId: int):
        roleAssignments = [assignment for assignment in self.userRoleAssignments if assignment.userId == userId]

        groupedRoles = {}

        for assignment in roleAssignments:
            if assignment.roleId not in groupedRoles:
                groupedRoles[assignment.roleId] = {
                    "role": next((role for role in self.roles if role.id == assignment.roleId), None),
                    "bankIds": []
                }
            if assignment.bankId and (assignment.bankId not in groupedRoles[assignment.roleId]["bankIds"]):
                groupedRoles[assignment.roleId]["bankIds"].append(assignment.bankId) 

        rolesWithBanks = [
            {
                "role": groupedRoles[roleId]["role"],
                "bankIds": groupedRoles[roleId]["bankIds"]
            }
            for roleId in groupedRoles
        ]

        return rolesWithBanks
    
    def getUserRoleAssignment(self, userId: int, bankId: str, roleId: int = None):
        for assignment in self.userRoleAssignments:
            if assignment.userId == userId and assignment.bankId == bankId:
                print(f"User {userId} has role {assignment.roleId} assigned for bank {bankId}.")
                return assignment
        return None
    
    def removeUser(self, username: str):
        for i,user in enumerate(self.users):
            if user.username == username:
                self.users.pop(i)
            UserManager.setUsers(self.users)
            return True 
        return False