from abc import ABC, abstractmethod
from liceo.infra.domain.vo import Paged
from . import dtos
from ..domain import entities


class ProjectService(ABC):
    @abstractmethod
    def filter_projects(self, dto: dtos.FilterProjectsDTO) -> Paged[entities.Project]:
        pass

    @abstractmethod
    def create_project(self, dto: dtos.CreateProjectDTO) -> entities.Project:
        pass
