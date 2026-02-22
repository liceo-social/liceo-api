from pydantic import BaseModel, Field
from liceo.infra.domain.vo import Pagination
from ..application import dtos


class FilterPermissionsRequest(BaseModel):
    name: str | None = Field(default=None)
    max: int
    page: int

    def to_dto(self) -> dtos.FilterPermissionsDTO:
        return dtos.FilterPermissionsDTO(
            name=self.name,
            pagination=Pagination(
                max=self.max,
                page=self.page
            )
        )
