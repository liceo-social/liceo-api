from liceo.infra.domain.entities import AuditInfo
from ..domain import entities, vo


def from_row_to_project(row: dict) -> entities.Project | None:
    print(row)
    if not row:
        return
    project = entities.Project(vo.ProjectId(row["id"]))
    project._version = row["version"]
    project.name = row["name"]
    project.description = row["description"]
    project.audit = AuditInfo(created_by=vo.UserId(row["created_by"]))
    project.audit.created_at = row["created_at"]
    return project


def from_row_to_project_coordinator(row: dict) -> entities.ProjectCoordinator:
    coordinator = entities.ProjectCoordinator(vo.ProjectCoordinatorId(row["id"]))
    coordinator._version = row["version"]
    coordinator.project = vo.ProjectId(row["project_id"])
    coordinator.user = vo.UserId(row["user_id"])
    coordinator.is_owner = row["is_owner"]
    coordinator.audit = AuditInfo(created_by=vo.UserId(row["created_by"]))
    coordinator.audit.created_at = row["created_at"]
    return coordinator
