from pydantic import BaseModel, Field
from liceo.infra.domain.vo import Pagination
from liceo.security.common.adapters.di import UserInfo
from liceo.security.common.application.dto import CurrentUserDTO
from ..application.dtos import CreateUserCaseDTO
from ..domain.vo import UserId
from ..application.dtos import FilterUsersDTO


class CreateUserFields(BaseModel):
    name: str
    surname: str
    photo: str | None
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
            photo=self.fields.photo,
            password=self.fields.password,
            roles=self.fields.roles,
            created_by=CurrentUserDTO(
                id=self.created_by.id,
                roles=self.created_by.roles,
                is_admin=self.created_by.is_admin
            )
        )


class FilteringUsersRequest(BaseModel):
    max: int = Field(100, gt=0, le=100)
    page: int = Field(0, ge=0)
    name: str | None = None
    surname: str | None = None
    username: str | None = None

    def to_pagination(self):
        return Pagination(self.max, self.page)

    def toDTO(self):
        return FilterUsersDTO(
            name=self.name,
            surname=self.surname,
            username=self.username,
            pagination=self.to_pagination()
        )
