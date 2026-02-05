from dataclasses import dataclass


@dataclass
class CurrentUserDTO:
    id: str
    is_admin: bool
    roles: list[str]
