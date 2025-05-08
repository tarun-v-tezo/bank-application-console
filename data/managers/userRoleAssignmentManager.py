from models.User import User
from ..database import Database
from common.constants import DataKeys


class UserRoleAssignmentManager:
    __userRoleAssignments = []

    @classmethod
    def initialize(cls):
        cls.__userRoleAssignments = [User(**assignment) for assignment in Database.getData(DataKeys.USERROLEASSIGNMENTS)]

    @classmethod
    def getUsers(cls):
        return cls.__userRoleAssignments.copy()

    @classmethod
    def setUsers(cls, users):
        cls.__userRoleAssignments = users
        Database.setData(DataKeys.USERROLEASSIGNMENTS, cls.__userRoleAssignments)