from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    id: str


class ListUsersResponse(BaseModel):
    data: list[str]
