from shortuuid import uuid
from liceo.security.permissions.application import ports


class ShortIdGenerator(ports.GenerateIdPort):
    def next_id(self) -> str:
        return uuid()


class DummySecurityService(ports.SecurityPort):
    def check_permissions(self, permissions: list[str], id: str):
        return None
