from pydantic import BaseModel
from ..domain.entities import User


class CreateUserResponse(BaseModel):
    id: str

    @staticmethod
    def from_user(user: User):
        return CreateUserResponse(id=user.id.id)


class ListUsersResponse(BaseModel):
    data: list[str]
