from typing import Annotated
from fastapi import Depends, Body, Query, Path
from liceo.security.users.adapters.di import UsersServiceDependency
from liceo.infra.adapters.di import ConnectionFactoryDependency, ConnectionManagerDependency, TransactionManagerDependency, EventStoreDependency
from liceo.security.common.adapters.di import UserInfo
from ..application.repository import ProjectRepository, ProjectMemberRepository, ProjectCoordinatorRepository
from ..application.service import ProjectService
from .repository import SQLProjectRepository, SQLProjectMemberRepository, SQLProjectCoordinatorRepository
from .service import DatabaseAwareProjectService
from .requests import CreateProjectRequest, CreateProjectDetails, ListProjectsRequest, AddMemberToProjectRequest, AddMemberToProjectPath, AddCoordinatorRequest, AddCoordinatorPayload, FindAllCoordinatorsByProjectsRequest

# ------ REPOSITORIES


def create_project_repository(factory: ConnectionFactoryDependency) -> ProjectRepository:
    return SQLProjectRepository(factory=factory)


ProjectRepositoryDependency = Annotated[ProjectRepository, Depends(
    create_project_repository)]


def create_project_members_repository(factory: ConnectionFactoryDependency) -> ProjectMemberRepository:
    return SQLProjectMemberRepository(factory=factory)


ProjectMemberRepositoryDependency = Annotated[ProjectMemberRepository, Depends(
    create_project_members_repository)]


def create_project_coordinators_repository(factory: ConnectionFactoryDependency) -> ProjectCoordinatorRepository:
    return SQLProjectCoordinatorRepository(factory=factory)


ProjectCoordinatorRepositoryDependency = Annotated[ProjectCoordinatorRepository, Depends(
    create_project_coordinators_repository)]

# ------ SERVICES


def create_project_service(
        projects: ProjectRepositoryDependency,
        users: UsersServiceDependency,
        project_members: ProjectMemberRepositoryDependency,
        project_coordinators: ProjectCoordinatorRepositoryDependency,
        transaction_manager_factory: TransactionManagerDependency,
        connection_manager_factory: ConnectionManagerDependency,
        event_store: EventStoreDependency
) -> ProjectService:
    return DatabaseAwareProjectService(
        projects=projects,
        users=users,
        project_members=project_members,
        project_coordinators=project_coordinators,
        transaction_manager_factory=transaction_manager_factory,
        connection_manager_factory=connection_manager_factory,
        event_store=event_store
    )


ProjectServiceDependency = Annotated[ProjectService, Depends(create_project_service)]

# ------ REQUESTS


def create_project_request(
        user_info: UserInfo,
        details: CreateProjectDetails = Body()
) -> CreateProjectRequest:
    return CreateProjectRequest(created_by=user_info, details=details)


CreateProjectRequestDependency = Annotated[CreateProjectRequest, Depends(
    create_project_request)]


ListProjectsRequestDependency = Annotated[ListProjectsRequest, Query()]


def created_add_project_member_request(
        user_info: UserInfo,
        details: AddMemberToProjectPath = Path()
):
    return AddMemberToProjectRequest(created_by=user_info, details=details)


AddMemberToProjectRequestDependency = Annotated[AddMemberToProjectRequest, Depends(
    created_add_project_member_request)]


def create_add_cordinator_payload(
        id: str = Path(),
        user_id: str = Path()
):
    return AddCoordinatorPayload(id=id, user_id=user_id)


def create_add_coordinator_request(
        user_info: UserInfo,
        is_owner: bool = Body(),
        payload: AddCoordinatorPayload = Depends(create_add_cordinator_payload)
):
    return AddCoordinatorRequest(added_by=user_info, details=payload, is_owner=is_owner)


AddCoordinatorRequestDependency = Annotated[AddCoordinatorRequest, Depends(
    create_add_coordinator_request)]


FindAllCoordinatorsByProjectsRequestDependency = Annotated[FindAllCoordinatorsByProjectsRequest, Body(
)]
