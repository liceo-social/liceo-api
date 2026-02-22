from liceo.infra.adapters.rest.endpoints import RestGroupSpec
from liceo.infra.domain.vo import Paged
from liceo.security.common.adapters.di import has_permission


from . import di, permissions, responses

specs = RestGroupSpec(
    name="PERMISSIONS",
    path="/permissions",
    description="Operations for maging permissions",
)

router = specs.create_router()


@router.get(
    path="/",
    dependencies=[has_permission(permissions.PERMISSIONS_LIST)]
)
def list(
    request: di.FilterPermissionsRequestDependency,
    service: di.PermissionsServiceDependency
) -> responses.FilterPermissionsResponse:
    return responses.FilterPermissionsResponse.from_paged(service.filter(request.to_dto()))
