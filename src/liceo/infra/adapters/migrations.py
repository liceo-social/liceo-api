from dataclasses import dataclass
from pathlib import Path

from liceo.labs.db.core import ConnectionFactory
from liceo.labs.migrations.core import DBM


@dataclass
class MigrationLoader:
    connection_factory: ConnectionFactory

    def apply(self):
        migrations_path = Path(__file__).parent / "migrations"
        db_migrations = DBM(
            connection_factory=self.connection_factory, path=migrations_path)
        db_migrations.create_db().apply_migrations()
