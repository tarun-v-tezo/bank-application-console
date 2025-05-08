from dataclasses import dataclass


@dataclass
class NewUserRequest:
    username: str
    password: str
    name: str