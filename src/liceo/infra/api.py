from typing import cast

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from liceo.infra.adapters.di import MigrationsDependency
from liceo.infra.adapters.di_scheduler import SchedulerDependency
from liceo.infra.adapters.error_handlers import liceo_handler
from liceo.infra.adapters.tracing import init_tracing
from liceo.infra.domain.error import I18Error
from liceo.infra.domain.vo import ConfigurationSingleton
from liceo.labs.decorators import solve_lifespan
from liceo.security.users.adapters import endpoints as users_api
from liceo.security.roles.adapters import endpoints as roles_api
from liceo.security.authentication.adapters import endpoints as auth_api
from liceo.storage.adapters import endpoints as storage_api

OPENAPI = {
    "title": "LICEO API",
    "version": "1.0.0",
    "description": """
This is a collection of REST endpoints to be used by developers and Liceo's
UI to access the Liceo platform.
    """,
    "openapi_tags": [
        auth_api.specs.metadata(),
        users_api.specs.metadata(),
        roles_api.specs.metadata(),
        storage_api.specs.metadata()
    ],
}


def init_v1_endpoints():
    """
    collects all API V1 endpoints
    """
    v1 = APIRouter(prefix="/v1")
    v1.include_router(auth_api.router)
    v1.include_router(users_api.router)
    v1.include_router(roles_api.router)
    v1.include_router(storage_api.router)
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
        I18Error, lambda r, x: liceo_handler(r, cast(I18Error, x))
    )
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return api


def init():
    """
    initializes the whole application and static resources
    """
    # TRACING
    init_tracing(ConfigurationSingleton.instance())
    return init_app()
