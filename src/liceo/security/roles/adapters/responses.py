from dataclasses import dataclass
from liceo.infra.domain.vo import Paged
from ..application.dtos import RoleDTO


@dataclass
class ListRolesResponses:
    data: list[RoleDTO]
    total_count: int

    @staticmethod
    def from_dto(paged: Paged):
        return ListRolesResponses(data=paged.data, total_count=paged.total)
