from liceo.infra.domain.entities import AuditInfo
from ..domain import entities, vo


def from_row_to_project(row: dict) -> entities.Project:
    project = entities.Project(vo.ProjectId(row["id"]))
    project.name = row["name"]
    project.description = row["description"]
    project.audit = AuditInfo(created_by=vo.UserId(row["created_by"]))
    project.audit.created_at = row["created_at"]
    return project
