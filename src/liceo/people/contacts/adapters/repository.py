from shortuuid import uuid
from liceo.labs.db.sql import SQLRepository
from ..domain import vo, entities
from ..application import repository


class SQLContactRepository(repository.PersonContactRepository, SQLRepository):
    def generate_id(self) -> vo.PersonContactId:
        return vo.PersonContactId(id=uuid())

    def save_contact(self, contact: entities.PersonContact) -> entities.PersonContact | None:
        sql = self.resolve_sql(self.save_contact)
        self._get_connection().execute(
            sql=sql,
            params={
                "id": contact.id,
                "version": contact._version,
                "type": contact.type,
                "value": contact.value,
                "relationship": contact.relationship,
                "notes": contact.notes,
                "person_id": contact.person.id,
                "is_emergency": contact.is_emergency,
                "created_at": contact.created_at,
                "created_by": contact.created_by.id,
            }
        )
        return contact
