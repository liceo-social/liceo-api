from dataclasses import dataclass
from ..domain.vo import UserDetails


@dataclass
class CreateUserCaseDTO:
    name: str
    surname: str
    username: str
    password: str
    roles: list[str]
    created_by: UserDetails
