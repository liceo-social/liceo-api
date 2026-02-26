from datetime import datetime
from dataclasses import dataclass
from liceo.labs.sherlock.domain.entities import AggregateEvent
from liceo.infra.domain.entities import AuditableAggregate
from . import vo


class PersonIdentification(AuditableAggregate[vo.PersonIdentificationId, vo.UserId]):
    @dataclass
    class CreateIdCommand:
        id: vo.PersonIdentificationId
        person_id: str
        type: str
        value: str
        expiration_date: datetime | None
        created_by: str
        is_main_id: bool

    @dataclass(kw_only=True)
    class IdentificationCreated(AggregateEvent):
        event_type: str = "IDENTIFICATION_CREATED"
        value: str
        type: str
        person: vo.PersonId
        expiration_date: datetime | None
        is_main_id: bool
        created_by: vo.UserId

        def handle(self, aggregate: "PersonIdentification"):
            aggregate.mark_created_by(self.created_by)
            aggregate.type = self.type
            aggregate.value = self.value
            aggregate.person = self.person

    person: vo.PersonId
    type: str
    value: str

    @staticmethod
    def create(cmd: CreateIdCommand):
        return PersonIdentification(cmd.id).append(
            PersonIdentification.IdentificationCreated(
                event_by=vo.UserId(id=cmd.created_by),
                created_by=vo.UserId(id=cmd.created_by),
                type=cmd.type,
                value=cmd.value,
                expiration_date=cmd.expiration_date,
                person=vo.PersonId(id=cmd.person_id),
                is_main_id=cmd.is_main_id
            )
        )

    @property
    def aggregate_type(self) -> str:
        return "IDENTIFICATION"
