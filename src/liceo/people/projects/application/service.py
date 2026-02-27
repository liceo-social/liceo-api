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

    @abstractmethod
    def add_new_member(self, dto: dtos.AddMemberToProjectDTO) -> entities.ProjectMembership | None:
        pass

    @abstractmethod
    def add_coordinator(self, dto: dtos.AddCoordinatorToProjectDTO) -> entities.ProjectCoordinator | None:
        pass

    @abstractmethod
    def find_all_coordinators_by_project_ids(self, dto: dtos.FindAllCoordinatorsByProjectIdsDTO) -> Paged[entities.ProjectCoordinator]:
        pass
