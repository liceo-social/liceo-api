from jinja2 import Environment
from dataclasses import dataclass
from liceo.labs.logs import logged
from liceo.labs.sherlock.application.service import EventStoreService
from liceo.mail.domain.entities import Mail
from liceo.labs.db.core import AbstractService, managed_service, transactional, skip_default_connection

from ..application import repository, service, dtos


@dataclass
@managed_service
class DatabaseMailSchedulerService(service.MailScheduler, AbstractService):
    repository: repository.MailRepository
    event_store: EventStoreService

    @skip_default_connection
    @transactional()
    def queue_mail(self, input: dtos.QueueMailDTO) -> Mail:
        created = Mail.create(
            Mail.CreateMailCommand(
                id=self.repository.generate_id(),
                recipient=input.recipient,
                subject=input.subject,
                body=input.body,
                created_by=input.created_by
            )
        ).queue()

        queued = self.repository.save(created)
        self.event_store.append(queued)
        return queued


@dataclass
class Jinja2RendererService(service.TemplateRenderer):
    environment: Environment

    def render(self, template_name: str, content: dict) -> str:
        return self.environment.get_template(template_name).render(content)


class DevNullMailGateway(service.MailGateway, logged("liceo.mail.adapters.gateway.MailGateway")):
    def send(self, recipient: str, subject: str, content: str) -> None:
        self._logger.info("MAIL SENT")
