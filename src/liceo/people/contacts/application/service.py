from abc import ABC, abstractmethod
from ..domain import entities, vo
from . import dtos


class PersonContactService(ABC):
    @abstractmethod
    def save_contact(self, dto: dtos.CreatePersonContactDTO) -> entities.PersonContact:
        pass
