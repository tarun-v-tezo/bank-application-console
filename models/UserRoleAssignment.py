from dataclasses import dataclass
from typing import Optional

@dataclass
class UserRoleAssignment:
    id: int
    userId: int
    roleId: int
    bankId: Optional[str] = None