from shortuuid import uuid
from liceo.people.projects.domain.entities import Project
from liceo.labs.db.sql import SQLRepository
from liceo.people.projects.domain.vo import ProjectId
from ..application.repository import ProjectRepository


class SQLProjectRepository(ProjectRepository, SQLRepository):
    def generate_id(self) -> ProjectId:
        return ProjectId(uuid())

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
