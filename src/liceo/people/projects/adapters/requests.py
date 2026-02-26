from dataclasses import dataclass
from pydantic import BaseModel
from ..application import dtos
from liceo.security.common.adapters.requests import UserContextModel


class CreateProjectDetails(BaseModel):
    name: str
    description: str


class CreateProjectRequest(BaseModel):
    details: CreateProjectDetails
    created_by: UserContextModel

    def to_dto(self) -> dtos.CreateProjectDTO:
        return dtos.CreateProjectDTO(
            name=self.details.name,
            description=self.details.description,
            created_by=self.created_by.id
        )
