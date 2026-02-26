from shortuuid import uuid
from typing import override
from liceo.infra.domain.vo import Paged, Pagination
from liceo.people.projects.domain.entities import Project, ProjectMembership
from liceo.labs.db.sql import SQLRepository, sql
from liceo.people.projects.domain.vo import ProjectId, ProjectMembershipId
from ..application.repository import ProjectRepository, ProjectMemberRepository
from .mappers import from_row_to_project


class SQLProjectRepository(ProjectRepository, SQLRepository):
    @override
    def generate_id(self) -> ProjectId:
        return ProjectId(uuid())

    @sql(from_row_to_project)
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
        return Paged(
            total=result[0]["total_count"] if result else 0,
            data=list(map(from_row_to_project, result))
        )


class SQLProjectMemberRepository(ProjectMemberRepository, SQLRepository):
    def generate_id(self) -> ProjectMembershipId:
        return ProjectMembershipId(uuid())

    def save_membership(self, membership: ProjectMembership) -> ProjectMembership:
        self._get_connection().execute(
            sql=self.resolve_sql(self.save_membership),
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
