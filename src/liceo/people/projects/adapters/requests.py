from dataclasses import dataclass
from pydantic import BaseModel, Field
from ..application import dtos
from liceo.infra.domain.vo import Pagination
from liceo.security.common.adapters.requests import UserContextModel


class CreateProjectDetails(BaseModel):
    name: str
    description: str


class CreateProjectRequest(BaseModel):
    details: CreateProjectDetails
    created_by: UserContextModel

    def to_dto(self) -> dtos.CreateProjectDTO:
        return dtos.CreateProjectDTO(
            name=self.details.name,
            description=self.details.description,
            created_by=self.created_by.id
        )


class ListProjectsRequest(BaseModel):
    name: str | None = Field(default=None)
    max: int = Field(default=10, lt=20)
    page: int = Field(default=1)

    def to_dto(self) -> dtos.FilterProjectsDTO:
        return dtos.FilterProjectsDTO(
            name=self.name,
            pagination=Pagination(max=self.max, page=self.page)
        )
