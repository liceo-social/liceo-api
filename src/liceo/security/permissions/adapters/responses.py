from pydantic import BaseModel
from liceo.infra.domain.vo import Paged
from ..domain.entities import Permission


class PermissionResponse(BaseModel):
    id: str
    name: str
    description: str


class FilterPermissionsResponse(BaseModel):
    data: list[PermissionResponse]
    total_count: int

    @staticmethod
    def from_paged(paged: Paged[Permission]):
        return FilterPermissionsResponse(
            data=paged.map(
                lambda p: PermissionResponse(
                    id=p.id.id,
                    name=p.name,
                    description=p.description
                )
            ).data,
            total_count=paged.total
        )
