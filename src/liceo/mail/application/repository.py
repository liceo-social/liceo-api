from abc import abstractmethod
from ..domain.entities import Mail


class MailRepository:
    @abstractmethod
    def save(self, mail: Mail) -> Mail:
        pass

    @abstractmethod
    def fetch_pending(self) -> list[Mail]:
        pass

    @abstractmethod
    def mark_failed(self, mail: Mail) -> Mail:
        pass

    @abstractmethod
    def mark_sent(self, mail: Mail) -> Mail:
        pass

    @abstractmethod
    def generate_id(self) -> str:
        pass
