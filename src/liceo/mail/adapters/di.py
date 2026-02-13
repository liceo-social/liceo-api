from typing import Annotated
from fastapi import Depends
from liceo.infra.adapters.di import TransactionManagerDependency, ConnectionFactoryDependency, ConnectionManagerDependency, EventStoreDependency
from jinja2 import Environment, PackageLoader, select_autoescape
from ..application.service import MailGateway, MailScheduler, TemplateRenderer
from ..application.repository import MailRepository
from ..adapters.service import DevNullMailGateway, DatabaseMailSchedulerService, Jinja2RendererService
from ..adapters.repository import SQLMailRepository


def create_jinja2_environment():
    return Environment(
        loader=PackageLoader("liceo.mail.adapters"),
        autoescape=select_autoescape()
    )


Jinja2EnvironmentDependency = Annotated[Environment, Depends(create_jinja2_environment)]


def create_template_render(environment: Jinja2EnvironmentDependency):
    return Jinja2RendererService(environment=environment)


TemplateRenderDependency = Annotated[TemplateRenderer, Depends(create_template_render)]


def create_mail_gateway():
    return DevNullMailGateway()


MailGatewayDependency = Annotated[MailGateway, Depends(create_mail_gateway)]


def create_mail_repository(connection_factory: ConnectionFactoryDependency):
    return SQLMailRepository(factory=connection_factory)


MailRepositoryDependency = Annotated[MailRepository, Depends(create_mail_repository)]


def create_scheduler(
    connection_manager: ConnectionManagerDependency,
    transaction_manager: TransactionManagerDependency,
    repository: MailRepositoryDependency,
    event_store: EventStoreDependency
):
    return DatabaseMailSchedulerService(
        connection_manager=connection_manager,
        transaction_manager=transaction_manager,
        repository=repository,
        event_store=event_store
    )


MailSchedulerServiceDependency = Annotated[MailScheduler, Depends(create_scheduler)]
