from dataclasses import dataclass


@dataclass
class I18Error(Exception):
    code: str
    message: str


@dataclass
class ValidationError(I18Error):
    pass


class NotFoundError(I18Error):
    def __init__(self, entity_name: str, id: str = "unknown"):
        return super().__init__(
            "not_found.{}.{}".format(entity_name, id),
            "entity {} ({}) not found".format(entity_name, id),
        )


@dataclass
class NotAuthorizedError(I18Error):
    pass


@dataclass
class NotImplementedError(I18Error):
    def __init__(self):
        return super().__init__("not_implemented", "functionality not implemented")
