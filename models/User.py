
# class User:
#     def __init__(self, id: int, name: str, bankId: str, username: str, password: str, role: str):
#         self.id = id
#         self.name = name
#         self.bankId = bankId
#         self.username = username
#         self.password = password
#         self.role = role


from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    username: str
    password: str