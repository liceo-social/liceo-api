from pydantic import BaseModel


class CreatePermissionRequest(BaseModel):
    name: str
    description: str
