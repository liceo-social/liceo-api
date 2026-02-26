from dataclasses import dataclass
from typing import override
from liceo.infra.domain.entities import AuditableAggregate
from liceo.labs.sherlock.domain.entities import AggregateEvent
from . import vo


class Project(AuditableAggregate[vo.ProjectId, vo.UserId]):
    @dataclass
    class CreateProjectCommand:
        id: vo.ProjectId
        name: str
        description: str
        created_by: str

    @dataclass(kw_only=True)
    class ProjectCreated(AggregateEvent):
        event_type: str = "PROJECT_CREATED"
        name: str
        description: str
        created_by: str

        def handle(self, aggregate: "Project"):
            aggregate.mark_created_by(vo.UserId(self.created_by))
            aggregate.name = self.name
            aggregate.members_count = 0
            aggregate.description = self.description

    name: str
    description: str
    members_count: int

    @staticmethod
    def create(cmd: CreateProjectCommand) -> "Project":
        return Project(cmd.id).append(
            Project.ProjectCreated(
                name=cmd.name,
                description=cmd.description,
                created_by=cmd.created_by,
                event_by=vo.UserId(cmd.created_by)
            )
        )

    @property
    @override
    def aggregate_type(self) -> str:
        return "PROJECT"


class ProjectMembership(AuditableAggregate[vo.ProjectMembershipId, vo.UserId]):
    person: vo.PersonId
    project: vo.ProjectId
