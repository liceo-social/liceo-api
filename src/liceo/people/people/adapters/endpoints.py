from liceo.infra.adapters.rest.endpoints import RestGroupSpec, open_api_permissions
from liceo.security.common.adapters.di import has_permission

specs = RestGroupSpec(
    name="PEOPLE",
    path="/people",
    description="Operations for managing people",
)


router = specs.create_router()


@router.get(
    path="/",
    summary="List people",
    dependencies=[has_permission("!!!!!!!!!!!!!!!!!!")],
    openapi_extra={**open_api_permissions(["!!!!!!!!!!!!!!!"])}
)
def list(
    request: object,
    service: object
):
    pass


@router.post(
    path="/",
    summary="Add a new person",
    dependencies=[has_permission("!!!!!!!!!!!!!!!!!!")],
    openapi_extra={**open_api_permissions(["!!!!!!!!!!!!!!!"])}
)
def create(
    request: object,
    service: object
):
    pass
