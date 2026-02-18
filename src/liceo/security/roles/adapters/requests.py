from dataclasses import dataclass
from pydantic import Field, BaseModel
from liceo.infra.domain.vo import Pagination


class ListRolesRequest(BaseModel):
    max: int = Field(100, gt=0, le=100)
    page: int = Field(0, ge=0)

    def to_pagination(self):
        return Pagination(max=self.max, page=self.page)
