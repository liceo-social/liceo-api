from dataclasses import dataclass
from liceo.infra.domain.vo import Paged
from liceo.labs.db.core import AbstractService, managed_service, transactional
from liceo.labs.sherlock.application.service import EventStoreService
from liceo.people.projects.application.dtos import CreateProjectDTO, FilterProjectsDTO
from ..application.repository import ProjectRepository
from ..application.service import ProjectService
from ..domain import entities


@dataclass
@managed_service
class DatabaseAwareProjectService(ProjectService, AbstractService):
    repository: ProjectRepository
    event_store: EventStoreService

    @transactional()
    def create_project(self, dto: CreateProjectDTO) -> entities.Project:
        project = entities.Project.create(
            entities.Project.CreateProjectCommand(
                id=self.repository.generate_id(),
                name=dto.name,
                description=dto.description,
                created_by=dto.created_by
            )
        )

        self.repository.save_project(project)
        self.event_store.append(project)
        return project

    def filter_projects(self, dto: FilterProjectsDTO) -> Paged[entities.Project]:
        return self.repository.filter_projects_by_name(name=dto.name, pagination=dto.pagination)
