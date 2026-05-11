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
                event_by=cmd.created_by,
                created_by=cmd.created_by,
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
                projects=cmd.projects
            )
        )

    @property
    def aggregate_type(self) -> str:
        return "PERSON"
