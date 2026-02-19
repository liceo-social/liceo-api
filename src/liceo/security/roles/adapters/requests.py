from dataclasses import dataclass
from pydantic import Field, BaseModel
from liceo.infra.domain.vo import Pagination
from liceo.security.common.adapters.requests import UserContextModel

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


class CreateRoleRequestDetails(BaseModel):
    name: str
    description: str
    permissions: list[str]


class CreateRoleRequest(BaseModel):
    user: UserContextModel
    details: CreateRoleRequestDetails

    def to_dto(self):
        return dtos.CreateRoleDTO(
            name=self.details.name,
            description=self.details.description,
            is_admin=self.user.is_admin,
            created_by=self.user.id,
            permissions=self.details.permissions
        )


class UpdateRoleDetails(BaseModel):
    version: int
    name: str
    description: str


class UpdateRoleDetailsRequest(BaseModel):
    id: str
    user: UserContextModel
    details: UpdateRoleDetails

    def to_dto(self):
        return dtos.UpdateRoleDetailsDTO(
            id=self.id,
            version=self.details.version,
            name=self.details.name,
            description=self.details.description,
            updated_by=self.user.id,
            is_admin=self.user.is_admin
        )
