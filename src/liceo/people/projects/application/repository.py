from abc import ABC, abstractmethod
from ..domain import entities, vo


class ProjectRepository(ABC):
    @abstractmethod
    def generate_id(self) -> vo.ProjectId:
        pass

    @abstractmethod
    def save_project(self, project: entities.Project) -> entities.Project:
        pass
