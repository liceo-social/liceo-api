from dataclasses import dataclass
from liceo.infra.domain.entities import AuditableAggregate
from liceo.labs.sherlock.domain.entities import AggregateEvent

from . import vo, checks, errors


@dataclass(init=False)
class Person(AuditableAggregate[vo.PersonId, vo.UserId]):
    @dataclass
    class CreatePersonCommand(vo.BasicDetails):
        id: vo.PersonId
        main_id: vo.Identification | None
        emergency_contact: vo.EmergencyContact
        projects: list[vo.ProjectId]
        responsible: vo.UserId
        is_responsible_from_projects: bool
        created_by: vo.UserId

        def has_projects(self) -> bool:
            return self.projects is not None and len(self.projects) > 0

    @dataclass(kw_only=True)
    class PersonCreated(AggregateEvent, vo.BasicDetails):
        event_type: str = "PERSON_CREATED"
        main_id: vo.Identification | None
        emergency_contact: vo.EmergencyContact
        projects: list[vo.ProjectId]
        responsible: vo.UserId
        created_by: vo.UserId

        def handle(self, aggregate: "Person"):
            aggregate.mark_created_by(self.created_by)
            aggregate.basic_details = vo.BasicDetails(
                name=self.name,
                surname=self.surname,
                photo=self.photo,
                alias=self.alias,
                birthdate=self.birthdate,
                sex=self.sex,
                genre=self.genre
            )
            aggregate.emergency_contact = self.emergency_contact
            aggregate.main_id = self.main_id

    main_id: vo.Identification | None
    emergency_contact: vo.EmergencyContact
    basic_details: vo.BasicDetails
    projects: list[vo.ProjectId]
    responsible: vo.UserId

    @staticmethod
    def create(cmd: CreatePersonCommand):
        checks.check_basic_details(cmd)

        if not cmd.has_projects():
            raise errors.NoProjectsAttached()

        if not cmd.responsible:
            raise errors.NoResponsible()

        if not cmd.is_responsible_from_projects:
            raise errors.ResponsibleNotFromProjects()

        return Person(cmd.id).append(
            Person.PersonCreated(
                name=cmd.name,
                surname=cmd.surname,
                photo=cmd.photo,
                alias=cmd.alias,
                birthdate=cmd.birthdate,
                sex=cmd.sex,
                genre=cmd.genre,
                main_id=cmd.main_id,
                emergency_contact=cmd.emergency_contact,
                responsible=cmd.responsible,
                projects=cmd.projects,
                created_by=cmd.created_by
            )
        )

    @property
    def aggregate_type(self) -> str:
        return "PERSON"


class PersonContact(AuditableAggregate[vo.PersonContactId, vo.UserId]):
    @dataclass
    class CreateContactCommand:
        id: vo.PersonContactId
        person_id: str
        type: str
        value: dict
        is_emergency: bool
        created_by: str

    @dataclass(kw_only=True)
    class ContactCreated(AggregateEvent):
        event_type: str = "CONTACT_CREATED"
        person: vo.PersonId
        value: dict
        is_emergency: bool
        created_by: vo.UserId

        def handle(self, aggregate: "PersonContact"):
            aggregate.mark_created_by(self.created_by)
            aggregate.person = self.person
            aggregate.value = self.value
            aggregate.is_emergency = self.is_emergency

    person: vo.PersonId
    type: str
    value: dict
    is_emergency: bool

    @staticmethod
    def create(cmd: CreateContactCommand):
        return PersonContact(cmd.id).append(
            PersonContact.ContactCreated(
                person=vo.PersonId(id=cmd.person_id),
                value=cmd.value,
                is_emergency=cmd.is_emergency,
                created_by=vo.UserId(id=cmd.created_by)
            )
        )

    @property
    def aggregate_type(self) -> str:
        return "CONTACT"


class PersonIdentification(AuditableAggregate[vo.PersonIdentificationId, vo.UserId]):
    @dataclass
    class CreateIdCommand:
        id: vo.PersonIdentificationId
        person_id: str
        type: str
        value: str
        created_by: str
        is_main_id: bool

    @dataclass(kw_only=True)
    class IdentificationCreated(AggregateEvent):
        event_type: str = "IDENTIFICATION_CREATED"
        value: str
        type: str
        person: vo.PersonId
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
                type=cmd.type,
                value=cmd.value,
                person=vo.PersonId(id=cmd.person_id),
                created_by=vo.UserId(id=cmd.created_by),
                is_main_id=cmd.is_main_id
            )
        )

    @property
    def aggregate_type(self) -> str:
        return "IDENTIFICATION"
