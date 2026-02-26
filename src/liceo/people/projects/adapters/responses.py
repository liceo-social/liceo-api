from pydantic import BaseModel
from liceo.infra.domain.vo import Paged
from ..domain.entities import Project, ProjectMembership


class MinimalProjectResponse(BaseModel):
    id: str
    version: int

    @staticmethod
    def from_project(project: Project | None):
        if project:
            return MinimalProjectResponse(id=project.id.id, version=project._version)


class ProjectResponse(BaseModel):
    id: str
    version: int
    name: str
    description: str

    @staticmethod
    def from_project(project: Project):
        return ProjectResponse(
            id=project.id.id,
            version=project._version,
            name=project.name,
            description=project.description
        )


class ListProjectsResponse(BaseModel):
    data: list[ProjectResponse]
    total: int

    @staticmethod
    def from_paged(paged: Paged[Project]) -> "ListProjectsResponse":
        return ListProjectsResponse(
            data=paged.map(ProjectResponse.from_project).data,
            total=paged.total
        )


class ProjectMembershipResponse(BaseModel):
    id: str
    version: int
    person_id: str
    project_id: str

    @staticmethod
    def from_project_membership(membership: ProjectMembership | None):
        if membership:
            return ProjectMembershipResponse(
                id=membership.id.id,
                version=membership._version,
                person_id=membership.person.id,
                project_id=membership.project.id
            )
