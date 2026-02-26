from dataclasses import dataclass
from liceo.infra.domain.vo import Pagination


@dataclass
class CreateProjectDTO:
    name: str
    description: str
    created_by: str


@dataclass
class FilterProjectsDTO:
    name: str | None
    pagination: Pagination


@dataclass
class AddMemberToProjectDTO:
    project_id: str
    person_id: str
    created_by: str
