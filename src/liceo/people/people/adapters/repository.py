from shortuuid import uuid
from liceo.labs.db.sql import SQLRepository
from liceo.people.people.domain.entities import Person, PersonContact, PersonIdentification
from liceo.people.people.domain.vo import PersonContactId, PersonId, PersonIdentificationId

from ..application import repository


class SQLPersonRepository(repository.PersonRepository, SQLRepository):
    def generate_id(self) -> PersonId:
        return PersonId(id=uuid())

    def save_person(self, person: Person) -> Person | None:
        sql = self.resolve_sql(self.save_person)
        self._get_connection().execute(
            sql=sql,
            params={
                "id": person.id,
                "version": person._version,
                "name": person.basic_details.name,
                "surname": person.basic_details.surname,
                "photo": person.basic_details.photo,
                "alias": person.basic_details.alias,
                "birthdate": person.basic_details.birthdate,
                "sex": person.basic_details.sex,
                "genre": person.basic_details.genre,
                "responsible_id": person.responsible.id,
                "created_at": person.created_at,
                "created_by": person.created_by.id,
            }
        )
        return person


class SQLContactRepository(repository.PersonContactRepository, SQLRepository):
    def generate_id(self) -> PersonContactId:
        return PersonContactId(id=uuid())

    def save_contact(self, contact: PersonContact) -> PersonContact | None:
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


class SQLIdentificationRepository(repository.PersonIdentificationRepository, SQLRepository):
    def generate_id(self) -> PersonIdentificationId:
        return PersonIdentificationId(id=uuid())

    def save_identification(self, identification: PersonIdentification) -> PersonIdentification | None:
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
