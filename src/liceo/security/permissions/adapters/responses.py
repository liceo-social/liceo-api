from pydantic import BaseModel


class CreatePermissionResponse(BaseModel):
    id: str
    name: str
    description: str
