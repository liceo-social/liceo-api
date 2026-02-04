from dataclasses import dataclass
from pathlib import Path

from liceo.labs.db.core import ConnectionFactory, Transaction
from liceo.labs.migrations.core import DBM


@dataclass
class MigrationLoader:
    connection_factory: ConnectionFactory

    def apply(self):
        with Transaction(self.connection_factory):
            migrations_path = Path(__file__).parent / "migrations"
            db_migrations = DBM(
                connection=self.connection_factory.create(), path=migrations_path)
            # db_migrations.create_db().apply_migrations()
