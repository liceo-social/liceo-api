from abc import ABC, abstractmethod
from . import dtos
from ..domain import entities


class ProjectService(ABC):
    @abstractmethod
    def create_project(self, dto: dtos.CreateProjectDTO) -> entities.Project:
        pass
