from dataclasses import dataclass
from pydantic import BaseModel
from ..domain.entities import Project


@dataclass
class CreateProjectResponse(BaseModel):
    @staticmethod
    def from_project(project: Project):
        return CreateProjectResponse()
