from typing import Annotated
from fastapi import Depends, Query, Body, Path

from liceo.infra.adapters.di import ConnectionFactoryDependency, EventStoreDependency, ConnectionManagerDependency, TransactionManagerDependency
from liceo.security.common.adapters.di import SecurityServiceDependency, UserInfo
from liceo.mail.adapters.di import MailSchedulerServiceDependency, TemplateRenderDependency
from .repositories import SQLUsersRepository, SQLUsersImagesRepository
from .requests import CreateUserRequest, FilteringUsersRequest, UserDetails, UpdateUserRequest, UpdatePasswordRequest, UpdatePasswordFields, UpdateSecurityRequest, UpdateSecurityFields, ShowUserRequest
from .service import UsersService, SendActivationMailService
from ..application.repository import UsersRepository, UsersImagesRepository
from ..application.service import UserNotificationService

# ----- NOTIFICATIONS


def create_user_notifications(
        mails: MailSchedulerServiceDependency,
        templates: TemplateRenderDependency,
        connection_manager: ConnectionManagerDependency,
        transaction_manager: TransactionManagerDependency
):
    return SendActivationMailService(
        mails=mails,
        templates=templates,
        connection_manager=connection_manager,
        transaction_manager=transaction_manager
    )


NotificationsDependency = Annotated[UserNotificationService, Depends(
    create_user_notifications)]


# ----- REPOSITORIES
def repository(connection_factory: ConnectionFactoryDependency) -> UsersRepository:
    return SQLUsersRepository(factory=connection_factory)


RepositoryDependency = Annotated[UsersRepository, Depends(repository)]


def images_repository(connection_factory: ConnectionFactoryDependency) -> UsersImagesRepository:
    return SQLUsersImagesRepository(factory=connection_factory)


ImagesRepositoryDependency = Annotated[UsersImagesRepository, Depends(
    images_repository)]


# ---- SERVICES
def users_service(
    repository: RepositoryDependency,
    images_repository: ImagesRepositoryDependency,
    event_store: EventStoreDependency,
    security: SecurityServiceDependency,
    transaction_manager: TransactionManagerDependency,
    connection_manager: ConnectionManagerDependency,
    notifications: NotificationsDependency,
) -> UsersService:
    return UsersService(
        users=repository,
        images=images_repository,
        security=security,
        event_store=event_store,
        connection_manager=connection_manager,
        transaction_manager=transaction_manager,
        notifications=notifications
    )


UsersServiceDependency = Annotated[UsersService, Depends(users_service)]

# ------ REQUESTS

FilteringUsersRequestDependency = Annotated[FilteringUsersRequest, Query()]


def get_create_user_request(
    user: UserInfo,
    fields: UserDetails = Body()
):
    return CreateUserRequest(fields=fields, created_by=user)


CreateUserRequestDependency = Annotated[CreateUserRequest, Depends(
    get_create_user_request)]


def get_update_user_request(
        user: UserInfo,
        id: str = Path(),
        fields: UserDetails = Body()
):
    return UpdateUserRequest(id=id, fields=fields, updated_by=user)


UpdateUserRequestDependency = Annotated[UpdateUserRequest, Depends(
    get_update_user_request)]


def get_update_password_request(
        user: UserInfo,
        id: str = Path(),
        fields: UpdatePasswordFields = Body()
):
    return UpdatePasswordRequest(id=id, fields=fields, updated_by=user)


UpdatePasswordRequestDependency = Annotated[UpdatePasswordRequest, Depends(
    get_update_password_request)]


def get_update_security_request(
        user: UserInfo,
        id: str = Path(),
        fields: UpdateSecurityFields = Body()
):
    return UpdateSecurityRequest(id=id, updated_by=user, fields=fields)


UpdateSecurityRequestDependency = Annotated[UpdateSecurityRequest, Depends(
    get_update_security_request)]


def get_show_user_request(
        id: str = Path()
):
    return ShowUserRequest(id=id)


ShowUserRequestDependency = Annotated[ShowUserRequest, Depends(get_show_user_request)]
