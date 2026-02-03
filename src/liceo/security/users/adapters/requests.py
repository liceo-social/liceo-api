from pydantic import BaseModel

from ..application.dtos import CreateUserCaseDTO
from ..domain.vo import UserDetails


class CreateUserRequest(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    roles: list[str]
    created_by: UserDetails

    def to_input(self) -> CreateUserCaseDTO:
        return CreateUserCaseDTO(
            name=self.name,
            surname=self.surname,
            username=self.username,
            password=self.password,
            roles=self.roles,
            created_by=self.created_by
        )


class ListUsersRequest(BaseModel):
    pass
