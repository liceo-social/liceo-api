from abc import ABC, abstractmethod
from ..domain.entities import PersonIdentification
from .dtos import CreatePersonIdentificationDTO


class PersonIdentificationService(ABC):
    @abstractmethod
    def save_identification(self, dto: CreatePersonIdentificationDTO) -> PersonIdentification:
        pass
