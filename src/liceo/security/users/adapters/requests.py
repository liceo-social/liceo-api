from pydantic import BaseModel, Field
from liceo.infra.domain.vo import Pagination
from liceo.security.common.adapters.di import UserInfo
from ..application.dtos import CreateUserCaseDTO
from ..domain.vo import UserId
from ..application.dtos import FilterUsersDTO


class CreateUserFields(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    roles: list[str]


class CreateUserRequest(BaseModel):
    fields: CreateUserFields
    created_by: UserInfo

    def to_input(self) -> CreateUserCaseDTO:
        return CreateUserCaseDTO(
            name=self.fields.name,
            surname=self.fields.surname,
            username=self.fields.username,
            password=self.fields.password,
            roles=self.fields.roles,
            created_by=UserId(id=self.created_by.id)
        )


class FilteringUsersRequest(BaseModel):
    max: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    name: str | None = None
    surname: str | None = None
    username: str | None = None

    def to_pagination(self):
        return Pagination(self.max, self.offset)

    def toDTO(self):
        return FilterUsersDTO(
            name=self.name,
            surname=self.surname,
            username=self.username,
            pagination=self.to_pagination()
        )
