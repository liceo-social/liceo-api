from shortuuid import uuid
from typing import override
from liceo.infra.domain.vo import Paged, Pagination
from liceo.people.projects.domain.entities import Project, ProjectCoordinator, ProjectMembership
from liceo.labs.db.sql import SQLRepository, sql
from liceo.people.projects.domain.vo import ProjectCoordinatorId, ProjectId, ProjectMembershipId
from ..application.repository import ProjectRepository, ProjectMemberRepository, ProjectCoordinatorRepository
from . import mappers


class SQLProjectRepository(ProjectRepository, SQLRepository):
    @override
    def generate_id(self) -> ProjectId:
        return ProjectId(uuid())

    @sql(mappers.from_row_to_project)
    def find_project_by_id(self, id: str) -> Project | None:
        return None

    @override
    def save_project(self, project: Project) -> Project:
        self._get_connection().execute(
            self.resolve_sql(self.save_project),
            params={
                "id": project.id.id,
                "version": project._version,
                "name": project.name,
                "description": project.description,
                "created_by": project.created_by.id,
                "created_at": project.created_at
            }
        )
        return project

    @override
    def filter_projects_by_name(self, name: str | None, pagination: Pagination) -> Paged[Project]:
        sql = self.resolve_sql(self.filter_projects_by_name)
        params: dict = {
            "max": pagination.max,
            "offset": pagination.get_offset()
        }

        if name:
            params.update({"name": f"%{name}%"})

        result = self._get_connection().all(
            self.sql_optimize_params(sql, params),
            params
        )
        transformed = list(map(mappers.from_row_to_project, result))
        return Paged(
            total=result[0]["total_count"] if result else 0,
            data=[t for t in transformed if t]
        )


class SQLProjectMemberRepository(ProjectMemberRepository, SQLRepository):
    def generate_id(self) -> ProjectMembershipId:
        return ProjectMembershipId(uuid())

    def save_project_membership(self, membership: ProjectMembership) -> ProjectMembership:
        self._get_connection().execute(
            sql=self.resolve_sql(self.save_project_membership),
            params={
                "id": membership.id,
                "version": membership._version,
                "project_id": membership.project.id,
                "person_id": membership.person.id,
                "created_by": membership.created_by,
                "created_at": membership.created_at
            }
        )
        return membership


class SQLProjectCoordinatorRepository(ProjectCoordinatorRepository, SQLRepository):
    def generate_id(self) -> ProjectCoordinatorId:
        return ProjectCoordinatorId(uuid())

    def save_project_coordinator(self, project_coordinator: ProjectCoordinator) -> ProjectCoordinator | None:
        self._get_connection().execute(
            sql=self.resolve_sql(self.save_project_coordinator),
            params={
                "id": project_coordinator.id.id,
                "version": project_coordinator._version,
                "project_id": project_coordinator.project.id,
                "user_id": project_coordinator.user.id,
                "is_owner": project_coordinator.is_owner,
                "created_by": project_coordinator.created_by.id,
                "created_at": project_coordinator.created_at
            }
        )
        return project_coordinator

    def find_all_coordinators_by_project_ids(self, project_ids: list[str]) -> Paged[ProjectCoordinator]:
        sql = self.resolve_sql(self.find_all_coordinators_by_project_ids)
        rows = self._get_connection().all(
            sql=sql,
            params={
                "ids": project_ids
            }
        )

        if not rows or len(rows) <= 0:
            return Paged.empty()

        return Paged(
            total=rows[0]["total_count"],
            data=list(
                map(
                    mappers.from_row_to_project_coordinator,
                    rows
                )
            )
        )
