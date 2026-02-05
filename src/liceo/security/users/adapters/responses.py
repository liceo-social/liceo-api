from pydantic import BaseModel
from liceo.infra.domain.vo import Paged
from ..domain.entities import User
from .repositories import UserDTO


class CreateUserResponse(BaseModel):
    id: str

    @staticmethod
    def from_user(user: User):
        return CreateUserResponse(id=user.id.id)


class ListUsersResponse(BaseModel):
    data: list[UserDTO]
    total_count: int

    @staticmethod
    def fromDTO(dto: Paged[UserDTO]):
        return ListUsersResponse(data=dto.data, total_count=dto.total)
