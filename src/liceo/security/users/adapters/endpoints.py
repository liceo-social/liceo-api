from liceo.infra.adapters.rest.endpoints import RestGroupSpec


specs = RestGroupSpec(
    name="USERS",
    path="/sec/users",
    description="Operations for maging a user in the system",
)


router = specs.create_router()


@router.get("/")
def list_users(requester: object, service: object):
    pass


@router.post("/")
def create_user(
    requester: object, request: object, service: object
):
    pass
