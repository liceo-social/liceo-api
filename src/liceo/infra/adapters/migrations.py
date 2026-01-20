from dataclasses import dataclass
from pathlib import Path

from liceo.labs.db.core import Connection
from liceo.labs.migrations.core import DBM


@dataclass
class MigrationLoader:
    connection: Connection

    def apply(self):
        with self.connection.begin() as conn:
            migrations_path = Path(__file__).parent / "migrations"
            db_migrations = DBM(connection=conn, path=migrations_path)
            db_migrations.create_db().apply_migrations()
