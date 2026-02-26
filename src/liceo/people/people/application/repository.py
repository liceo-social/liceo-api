from abc import ABC, abstractmethod
from ..domain import entities, vo


class PersonRepository(ABC):
    @abstractmethod
    def generate_id(self) -> vo.PersonId:
        pass

    @abstractmethod
    def save_person(self, person: entities.Person) -> entities.Person | None:
        pass
