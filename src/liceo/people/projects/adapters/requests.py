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


class AddMemberToProjectPath(BaseModel):
    id: str
    person_id: str


class AddMemberToProjectRequest(BaseModel):
    created_by: UserContextModel
    details: AddMemberToProjectPath

    def to_dto(self) -> dtos.AddMemberToProjectDTO:
        return dtos.AddMemberToProjectDTO(
            project_id=self.details.id,
            person_id=self.details.person_id,
            created_by=self.created_by.id
        )


class AddCoordinatorPayload(BaseModel):
    id: str
    user_id: str


class AddCoordinatorRequest(BaseModel):
    added_by: UserContextModel
    is_owner: bool = Field(default=False)
    details: AddCoordinatorPayload

    def to_dto(self) -> dtos.AddCoordinatorToProjectDTO:
        return dtos.AddCoordinatorToProjectDTO(
            user_id=self.details.user_id,
            project_id=self.details.id,
            added_by=self.added_by.id,
            is_owner=self.is_owner
        )


class FindAllCoordinatorsByProjectsRequest(BaseModel):
    projects: list[str]

    def to_dto(self) -> dtos.FindAllCoordinatorsByProjectIdsDTO:
        return dtos.FindAllCoordinatorsByProjectIdsDTO(projects=self.projects)
