from dataclasses import dataclass
from pydantic import Field, BaseModel
from liceo.infra.domain.vo import Pagination
from ..application import dtos


class ListRolesRequest(BaseModel):
    max: int = Field(100, gt=0, le=100)
    page: int = Field(0, ge=0)

    def to_pagination(self):
        return Pagination(max=self.max, page=self.page)


class ShowRoleRequest(BaseModel):
    id: str

    def to_dto(self) -> dtos.ShowRoleDTO:
        return dtos.ShowRoleDTO(id=self.id)
