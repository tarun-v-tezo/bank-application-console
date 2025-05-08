from models.Roles import Role
from ..database import Database
from common.constants import DataKeys


class RoleManager:
    __roles = []

    @classmethod
    def initialize(cls):
        cls.__roles = [Role(**roleData) for roleData in Database.getData(DataKeys.ROLES)]

    @classmethod
    def getRoles(cls):
        return cls.__roles.copy()

    @classmethod
    def setRoles(cls, roles):
        cls.__roles = roles
        Database.setData(DataKeys.ROLES, cls.__roles)