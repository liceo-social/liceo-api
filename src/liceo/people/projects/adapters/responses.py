from pydantic import BaseModel
from liceo.infra.domain.vo import Paged
from ..domain.entities import Project


class SimpleProjectResponse(BaseModel):
    id: str
    version: int
    name: str
    description: str

    @staticmethod
    def from_project(project: Project):
        return SimpleProjectResponse(
            id=project.id.id,
            version=project._version,
            name=project.name,
            description=project.description
        )


class CreateProjectResponse(SimpleProjectResponse):
    pass


class ListProjectsResponse(BaseModel):
    data: list[SimpleProjectResponse]
    total: int

    @staticmethod
    def from_paged(paged: Paged[Project]) -> "ListProjectsResponse":
        return ListProjectsResponse(
            data=paged.map(SimpleProjectResponse.from_project).data,
            total=paged.total
        )
