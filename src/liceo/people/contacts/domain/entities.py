from dataclasses import dataclass
from liceo.labs.sherlock.domain.entities import AggregateEvent
from liceo.infra.domain.entities import AuditableAggregate
from . import vo


class PersonContact(AuditableAggregate[vo.PersonContactId, vo.UserId]):
    @dataclass
    class CreateContactCommand:
        id: vo.PersonContactId
        person_id: str
        type: str
        relationship: str
        value: str
        notes: str | None
        is_emergency: bool
        created_by: str

    @dataclass(kw_only=True)
    class ContactCreated(AggregateEvent):
        event_type: str = "CONTACT_CREATED"
        person: vo.PersonId
        type: str
        relationship: str
        value: str
        notes: str | None
        is_emergency: bool
        created_by: vo.UserId

        def handle(self, aggregate: "PersonContact"):
            aggregate.mark_created_by(self.created_by)
            aggregate.person = self.person
            aggregate.type = vo.ContactType(self.type)
            aggregate.relationship = vo.ContactRelationship(self.relationship)
            aggregate.value = self.value
            aggregate.is_emergency = self.is_emergency

    person: vo.PersonId
    type: vo.ContactType
    relationship: vo.ContactRelationship
    value: str
    notes: str
    is_emergency: bool

    @staticmethod
    def create(cmd: CreateContactCommand):
        return PersonContact(cmd.id).append(
            PersonContact.ContactCreated(
                event_by=vo.UserId(id=cmd.created_by),
                created_by=vo.UserId(id=cmd.created_by),
                person=vo.PersonId(id=cmd.person_id),
                type=cmd.type,
                relationship=cmd.relationship,
                value=cmd.value,
                notes=cmd.notes,
                is_emergency=cmd.is_emergency,
            )
        )

    @property
    def aggregate_type(self) -> str:
        return "CONTACT"
