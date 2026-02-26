from shortuuid import uuid
from liceo.labs.db.sql import SQLRepository
from ..domain import vo, entities
from ..application import repository


class SQLIdentificationRepository(repository.PersonIdentificationRepository, SQLRepository):
    def generate_id(self) -> vo.PersonIdentificationId:
        return vo.PersonIdentificationId(id=uuid())

    def save_identification(self, identification: entities.PersonIdentification) -> entities.PersonIdentification | None:
        sql = self.resolve_sql(self.save_identification)
        self._get_connection().execute(
            sql=sql,
            params={
                "id": identification.id,
                "version": identification._version,
                "type": identification.type,
                "value": identification.value,
                "person_id": identification.person.id,
                "created_at": identification.created_at,
                "created_by": identification.created_by.id
            }
        )
        return identification
