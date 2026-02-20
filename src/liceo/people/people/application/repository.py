from abc import ABC, abstractmethod
from ..domain import entities, vo


class PersonRepository(ABC):
    @abstractmethod
    def generate_id(self) -> vo.PersonId:
        pass

    @abstractmethod
    def save_person(self, person: entities.Person) -> entities.Person | None:
        pass


class PersonContactRepository(ABC):
    @abstractmethod
    def generate_id(self) -> vo.PersonContactId:
        pass

    @abstractmethod
    def save_contact(self, contact: entities.PersonContact) -> entities.PersonContact | None:
        pass


class PersonIdentificationRepository(ABC):
    @abstractmethod
    def generate_id(self) -> vo.PersonIdentificationId:
        pass

    @abstractmethod
    def save_identification(self, identification: entities.PersonIdentification) -> entities.PersonIdentification | None:
        pass
