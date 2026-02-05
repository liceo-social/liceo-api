from typing import List
from pydantic import BaseModel, Field


class UserContextModel(BaseModel):
    id: str = Field(default="")
    roles: List[str] = Field(default=[])
    is_admin: bool = Field(default=False)

    @staticmethod
    def empty():
        return UserContextModel()
