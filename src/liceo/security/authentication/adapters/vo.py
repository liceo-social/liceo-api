from pydantic import BaseModel, Field


class UserContextModel(BaseModel):
    id: str = Field(default="")
    username: str = Field(default="")
    roles: list[str] = Field(default=[])

    @staticmethod
    def empty():
        return UserContextModel()
