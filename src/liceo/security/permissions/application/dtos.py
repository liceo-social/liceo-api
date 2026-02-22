from dataclasses import dataclass
from liceo.infra.domain.vo import Pagination


@dataclass
class FilterPermissionsDTO:
    name: str | None
    pagination: Pagination
