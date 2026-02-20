from abc import ABC, abstractmethod
from ..domain import entities, vo


class PersonRepository(ABC):
    @abstractmethod
    def generate_id(self) -> vo.PersonId:
        pass

    @abstractmethod
    def save(self, person: entities.Person) -> entities.Person | None:
        pass


class PersonContactRepository(ABC):
    @abstractmethod
    def generate_id(self) -> vo.PersonContactId:
        pass

    @abstractmethod
    def save(self, contact: entities.PersonContact) -> entities.PersonContact | None:
        pass


class PersonIdentificationRepository(ABC):
    @abstractmethod
    def generate_id(self) -> vo.PersonIdentificationId:
        pass

    @abstractmethod
    def save(self, identification: entities.PersonIdentification) -> entities.PersonIdentification | None:
        pass
