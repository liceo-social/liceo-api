from dataclasses import dataclass
from liceo.infra.domain.vo import Paged
from liceo.labs.db.core import AbstractService, managed_service, transactional
from liceo.labs.sherlock.application.service import EventStoreService
from liceo.security.users.application.service import AbstractUsersService
from liceo.security.users.application.dtos import GetUserDTO
from liceo.people.projects.application.dtos import AddCoordinatorToProjectDTO, AddMemberToProjectDTO, CreateProjectDTO, FilterProjectsDTO, FindAllCoordinatorsByProjectIdsDTO
from ..application.repository import ProjectRepository, ProjectMemberRepository, ProjectCoordinatorRepository
from ..application.service import ProjectService
from ..domain import entities


@dataclass
@managed_service
class DatabaseAwareProjectService(ProjectService, AbstractService):
    projects: ProjectRepository
    project_members: ProjectMemberRepository
    project_coordinators: ProjectCoordinatorRepository
    users: AbstractUsersService
    event_store: EventStoreService

    @transactional()
    def create_project(self, dto: CreateProjectDTO) -> entities.Project:
        project = entities.Project.create(
            entities.Project.CreateProjectCommand(
                id=self.projects.generate_id(),
                name=dto.name,
                description=dto.description,
                created_by=dto.created_by
            )
        )

        self.projects.save_project(project)
        self.event_store.append(project)
        return project

    def filter_projects(self, dto: FilterProjectsDTO) -> Paged[entities.Project]:
        return self.projects.filter_projects_by_name(name=dto.name, pagination=dto.pagination)

    @transactional()
    def add_new_member(self, dto: AddMemberToProjectDTO) -> entities.ProjectMembership | None:
        project = self.projects.find_project_by_id(dto.project_id)

        if not project:
            return

        project_membership = entities.ProjectMembership.create(
            entities.ProjectMembership.CreateMembershipCommand(
                id=self.project_members.generate_id(),
                project_id=dto.project_id,
                person_id=dto.person_id,
                created_by=dto.created_by
            )
        )
        self.project_members.save_project_membership(project_membership)
        self.event_store.append(project_membership)
        return project_membership

    @transactional()
    def add_coordinator(self, dto: AddCoordinatorToProjectDTO) -> entities.ProjectCoordinator | None:
        project = self.projects.find_project_by_id(dto.project_id)

        if not project:
            return

        coordinator = self.users.get_user(GetUserDTO(dto.user_id))

        if not coordinator:
            return

        coordinator_to_add = entities.ProjectCoordinator.create(
            entities.ProjectCoordinator.CreateProjectCoordinatorCommand(
                id=self.project_coordinators.generate_id(),
                user_id=dto.user_id,
                project_id=dto.project_id,
                is_owner=dto.is_owner,
                added_by=dto.added_by
            )
        )
        self.project_coordinators.save_project_coordinator(coordinator_to_add)
        self.event_store.append(coordinator_to_add)
        return coordinator_to_add

    def find_all_coordinators_by_project_ids(self, dto: FindAllCoordinatorsByProjectIdsDTO) -> Paged[entities.ProjectCoordinator]:
        return self.project_coordinators.find_all_coordinators_by_project_ids(dto.projects)
