from dataclasses import dataclass


@dataclass
class OptiakError(Exception):
    code: str
    message: str


@dataclass
class ValidationError(OptiakError):
    pass


class NotFoundError(OptiakError):
    def __init__(self, entity_name: str, id: str = "unknown"):
        return super().__init__(
            "not_found.{}.{}".format(entity_name, id),
            "entity {} ({}) not found".format(entity_name, id),
        )


@dataclass
class NotAuthorizedError(OptiakError):
    pass
