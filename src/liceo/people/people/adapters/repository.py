from shortuuid import uuid
from liceo.labs.db.sql import SQLRepository
from liceo.people.people.domain.entities import Person
from liceo.people.people.domain.vo import PersonId

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
