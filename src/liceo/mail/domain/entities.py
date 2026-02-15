from dataclasses import dataclass
from datetime import datetime, timedelta
from liceo.labs.sherlock.domain.entities import Aggregate, AggregateEvent
from . import vo


class Mail(Aggregate[vo.MailId]):
    @dataclass
    class CreateMailCommand:
        id: str
        recipient: str
        subject: str
        body: str
        created_by: str

    @dataclass(kw_only=True)
    class MailCreated(AggregateEvent):
        event_type: str = "MAIL_CREATED"
        recipient: str
        subject: str
        body: str
        created_by: str

        def handle(self, aggregate: "Mail"):
            aggregate.recipient = self.recipient
            aggregate.subject = self.subject
            aggregate.body = self.body
            aggregate.created_at = datetime.now()
            aggregate.created_by = self.created_by

    @dataclass(kw_only=True)
    class MailQueued(AggregateEvent):
        event_type: str = "MAIL_QUEUED"

        def handle(self, aggregate: "Mail"):
            aggregate.status = "PENDING"
            aggregate.next_attempt_at = datetime.now()

    @dataclass
    class MarkMailAsFailedCommand:
        error: str

    @dataclass(kw_only=True)
    class MailFailed(AggregateEvent):
        event_type: str = "MAIL_FAILED"
        error: str

        def handle(self, aggregate: "Mail"):
            aggregate.last_error = self.error
            aggregate.next_attempt_at = datetime.now() + timedelta(minutes=2 ^ aggregate.retry_count)
            aggregate.retry_count = aggregate.retry_count + 1

    @dataclass
    class MarkMailAsSentCommand:
        pass

    @dataclass(kw_only=True)
    class MailSent(AggregateEvent):
        event_type: str = "MAIL_SENT"

        def handle(self, aggregate: "Mail"):
            aggregate.sent_at = datetime.now()
            aggregate.status = "SENT"

    recipient: str
    subject: str
    body: str
    status: str
    retry_count: int
    max_retries: int
    next_attempt_at: datetime
    last_error: str
    created_at: datetime
    created_by: str
    sent_at: datetime

    @staticmethod
    def create(cmd: CreateMailCommand):
        return Mail(vo.MailId(cmd.id)).append(
            Mail.MailCreated(
                recipient=cmd.recipient,
                subject=cmd.subject,
                body=cmd.body,
                created_by=cmd.created_by
            )
        )

    def queue(self):
        return self.append(Mail.MailQueued())

    def mark_failed(self, cmd: MarkMailAsFailedCommand):
        return self.append(Mail.MailFailed(error=cmd.error))

    def mark_sent(self):
        return self.append(Mail.MailSent())

    @property
    def aggregate_type(self) -> str:
        return "MAIL"
