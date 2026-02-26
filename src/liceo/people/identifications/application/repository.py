from abc import ABC, abstractmethod
from ..domain import entities, vo


class PersonIdentificationRepository(ABC):
    @abstractmethod
    def generate_id(self) -> vo.PersonIdentificationId:
        pass

    @abstractmethod
    def save_identification(self, identification: entities.PersonIdentification) -> entities.PersonIdentification | None:
        pass
