from pydantic import BaseModel, Field
from fastapi import Query
from typing import Annotated
from liceo.infra.domain.vo import Pagination
from ..application.dtos import CreateUserCaseDTO
from ..domain.vo import UserDetails
from ..application.dtos import FilterUsersDTO


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


class FilteringUsersRequestModel(BaseModel):
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


FilteringUsersRequest = Annotated[FilteringUsersRequestModel, Query()]
