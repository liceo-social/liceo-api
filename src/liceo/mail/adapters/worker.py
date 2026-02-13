from dataclasses import dataclass
from liceo.infra.application.output import EventStore
from ..application.repository import MailRepository
from ..application.service import MailGateway
from ..application.errors import MailGatewayError
from ..domain.entities import Mail


@dataclass
class MailWorker:
    repository: MailRepository
    gateway: MailGateway
    event_store: EventStore

    def process(self) -> None:
        for mail in self.repository.fetch_pending():
            try:
                # trying to send it
                self.gateway.send(
                    recipient=mail.recipient,
                    subject=mail.subject,
                    content=mail.body
                )
                self.repository.mark_sent(mail.mark_sent())
            except MailGatewayError as e:
                # if something happens we mark the db record
                self.repository.mark_failed(
                    mail.mark_failed(
                        Mail.MarkMailAsFailedCommand(e.code)
                    )
                )
            finally:
                # whatever happens goes to the audit trail
                self.event_store.append(mail)
