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
    data: list[str]

    @staticmethod
    def fromDTO(dto: Paged[UserDTO]):
        user_ids = list(map(lambda u: u.id, dto.data))
        return ListUsersResponse(data=user_ids)
