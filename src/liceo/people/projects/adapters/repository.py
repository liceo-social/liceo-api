from shortuuid import uuid
from typing import override
from liceo.infra.domain.vo import Paged, Pagination
from liceo.people.projects.domain.entities import Project
from liceo.labs.db.sql import SQLRepository
from liceo.people.projects.domain.vo import ProjectId
from ..application.repository import ProjectRepository
from .mappers import from_row_to_project


class SQLProjectRepository(ProjectRepository, SQLRepository):
    @override
    def generate_id(self) -> ProjectId:
        return ProjectId(uuid())

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

        result = self._get_connection().execute(
            self.sql_optimize_params(sql, params),
            params
        )
        return Paged(
            total=result[0]["total_count"] if result and result.rowcount > 0 else 0,
            data=list(map(from_row_to_project, result))
        )
