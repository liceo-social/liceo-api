from typing import Annotated, Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, Field

from liceo.infra.domain.vo import Paged, Pagination

T = TypeVar("T")
S = TypeVar("S", bound=Paged)


class PagedResponse(BaseModel, Generic[T]):
    paged: Paged[T]


class PaginationInput(BaseModel):
    max: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)

    def to_pagination(self):
        return Pagination(self.max, self.offset)


PaginationQuery = Annotated[PaginationInput, Query()]
