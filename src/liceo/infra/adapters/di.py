from typing import Annotated

from fastapi import Depends

from liceo.infra.adapters.persistence import SQLAlchemyConnection
from liceo.infra.domain.vo import OptiakConfiguration
from liceo.labs.db.core import Connection

from .migrations import MigrationLoader


# --8<-- [start:connection_dependency]
def load_connection(
    cfg: OptiakConfiguration = Depends(lambda: OptiakConfiguration()),
) -> Connection:
    return SQLAlchemyConnection(url=OptiakConfiguration().db.get_url())


ConnectionDependency = Annotated[Connection, Depends(load_connection)]
# --8<-- [end:connection_dependency]


# --8<-- [start:migrations_dependency]
def load_migration_loader(conn: ConnectionDependency):
    return MigrationLoader(conn)


MigrationsDependency = Annotated[MigrationLoader, Depends(load_migration_loader)]
# --8<-- [end:migrations_dependency]
