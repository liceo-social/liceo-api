from abc import ABC, abstractmethod
from ..domain import entities, vo


class PersonContactRepository(ABC):
    @abstractmethod
    def generate_id(self) -> vo.PersonContactId:
        pass

    @abstractmethod
    def save_contact(self, contact: entities.PersonContact) -> entities.PersonContact | None:
        pass
