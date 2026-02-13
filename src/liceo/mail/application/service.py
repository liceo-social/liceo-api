from abc import ABC, abstractmethod
from ..domain.entities import Mail
from .dtos import QueueMailDTO


class MailScheduler(ABC):
    @abstractmethod
    def queue_mail(self, input: QueueMailDTO) -> Mail:
        pass


class TemplateRenderer(ABC):
    @abstractmethod
    def render(self, template_name: str, content: dict) -> str:
        pass


class MailGateway(ABC):
    @abstractmethod
    def send(self, recipient: str, subject: str, content: str) -> None:
        pass
