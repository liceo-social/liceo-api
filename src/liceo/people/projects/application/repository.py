from abc import ABC, abstractmethod
from liceo.infra.domain.vo import Pagination, Paged
from ..domain import entities, vo


class ProjectRepository(ABC):
    @abstractmethod
    def generate_id(self) -> vo.ProjectId:
        pass

    @abstractmethod
    def save_project(self, project: entities.Project) -> entities.Project:
        pass

    @abstractmethod
    def filter_projects_by_name(self, name: str | None, pagination: Pagination) -> Paged[entities.Project]:
        pass
