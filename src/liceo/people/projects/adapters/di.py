from typing import Annotated
from fastapi import Depends, Body, Query
from liceo.infra.adapters.di import ConnectionFactoryDependency, ConnectionManagerDependency, TransactionManagerDependency, EventStoreDependency
from liceo.security.common.adapters.di import UserInfo
from ..application.repository import ProjectRepository
from ..application.service import ProjectService
from .repository import SQLProjectRepository
from .service import DatabaseAwareProjectService
from .requests import CreateProjectRequest, CreateProjectDetails, ListProjectsRequest

# ------ REPOSITORIES


def create_project_repository(factory: ConnectionFactoryDependency) -> ProjectRepository:
    return SQLProjectRepository(factory=factory)


ProjectRepositoryDependency = Annotated[ProjectRepository, Depends(
    create_project_repository)]


# ------ SERVICES


def create_project_service(
        repository: ProjectRepositoryDependency,
        transaction_manager_factory: TransactionManagerDependency,
        connection_manager_factory: ConnectionManagerDependency,
        event_store: EventStoreDependency
) -> ProjectService:
    return DatabaseAwareProjectService(
        repository=repository,
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
