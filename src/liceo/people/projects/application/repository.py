from abc import ABC, abstractmethod
from liceo.infra.domain.vo import Pagination, Paged
from ..domain import entities, vo


class ProjectRepository(ABC):
    @abstractmethod
    def generate_id(self) -> vo.ProjectId:
        pass

    @abstractmethod
    def find_project_by_id(self, id: str) -> entities.Project | None:
        pass

    @abstractmethod
    def save_project(self, project: entities.Project) -> entities.Project:
        pass

    @abstractmethod
    def filter_projects_by_name(self, name: str | None, pagination: Pagination) -> Paged[entities.Project]:
        pass


class ProjectMemberRepository(ABC):
    @abstractmethod
    def generate_id(self) -> vo.ProjectMembershipId:
        pass

    @abstractmethod
    def save_membership(self, membership: entities.ProjectMembership) -> entities.ProjectMembership:
        pass
