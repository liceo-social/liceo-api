from typing import cast

from fastapi import APIRouter, FastAPI

from optiak.infra.adapters.di import MigrationsDependency
from optiak.infra.adapters.di_scheduler import SchedulerDependency
from optiak.infra.adapters.error_handlers import optiak_handler
from optiak.infra.adapters.tracing import init_tracing
from optiak.infra.domain.error import OptiakError
from optiak.infra.domain.vo import ConfigurationSingleton
from optiak.labs.decorators import solve_lifespan
from optiak.security.auth.adapter.input import enpoints as auth_api
from optiak.security.registration.adapters import endpoints as registration_api

OPENAPI = {
    "title": "OPTIAK API",
    "version": "1.0.0",
    "description": """
This is a collection of REST endpoints to be used by developers and Optiak's
UI to access the Optiak platform.

## Get your API key

TODO

## Terms of use

TODO
    """,
    "openapi_tags": [
        auth_api.specs.metadata(),
        registration_api.specs.metadata(),
    ],
}


def init_v1_endpoints():
    """
    collects all API V1 endpoints
    """
    v1 = APIRouter(prefix="/v1")
    v1.include_router(auth_api.router)
    v1.include_router(registration_api.router)
    return v1


@solve_lifespan
async def init_scheduler(
    migrations: MigrationsDependency, scheduler: SchedulerDependency
):
    """
    inits scheduler and uses FastAPI life cycle to shutdown the
    scheduler once the application stops
    """
    migrations.apply()
    scheduler.start()

    yield
    scheduler.shutdown()


def init_app():
    """
    initializes FastAPI application instance

    - endpoints
    - error handlers
    """
    # API instance
    api = FastAPI(**OPENAPI, lifespan=init_scheduler)
    # Endpoints
    api.include_router(init_v1_endpoints())
    # Exception handlers
    api.add_exception_handler(
        OptiakError, lambda r, x: optiak_handler(r, cast(OptiakError, x))
    )
    return api


def init():
    """
    initializes the whole application and static resources
    """
    # TRACING
    init_tracing(ConfigurationSingleton.instance())
    return init_app()
