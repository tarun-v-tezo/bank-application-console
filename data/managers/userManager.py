from models.User import User
from ..database import Database
from common.constants import DataKeys


class UserManager:
    __users = []

    @classmethod
    def initialize(cls):
        cls.__users = [User(**userData) for userData in Database.getData(DataKeys.USERS)]

    @classmethod
    def getUsers(cls):
        return cls.__users.copy()

    @classmethod
    def setUsers(cls, users):
        cls.__users = users
        Database.setData(DataKeys.USERS, cls.__users)