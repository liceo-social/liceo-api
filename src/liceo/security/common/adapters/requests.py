from typing import List
from pydantic import BaseModel, Field


class UserContextModel(BaseModel):
    username: str = Field(default="")
    roles: List[str] = Field(default=[])

    @staticmethod
    def empty():
        return UserContextModel()
