from abc import ABC, abstractmethod
from . import dtos
from ..domain import entities


class PersonService(ABC):
    @abstractmethod
    def save_person(self, dto: dtos.CreatePersonDTO) -> entities.Person | None:
        pass
