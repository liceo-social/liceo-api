from abc import ABC, abstractmethod
from dataclasses import dataclass

from liceo.security.permissions.application import ports
from liceo.security.permissions.domain import vo
from liceo.security.permissions.domain.entities import Permission


class CreatePermissionCase(ABC):
    @dataclass
    class Input:
        name: str
        created_by: str
        description: str

    @dataclass
    class Output:
        id: str
        name: str
        description: str

        @staticmethod
        def from_entity(entity: Permission):
            return CreatePermissionCase.Output(
                id=entity.id.id,
                name=entity.name,
                description=entity.description
            )

    @abstractmethod
    def create_permission(self, input: Input) -> Output:
        pass


class CreatePermissionService(CreatePermissionCase):
    def __init__(
        self,
        id_gen_port: ports.GenerateIdPort,
        security_port: ports.SecurityPort,
        save_port: ports.SavePermissionPort
    ):
        self.save_port = save_port
        self.security_port = security_port
        self.id_gen_port = id_gen_port

    def create_permission(self, input: CreatePermissionCase.Input) -> CreatePermissionCase.Output:
        command = Permission.CreatePermissionCommand(
            name=input.name,
            next_id=self.id_gen_port.next_id,
            created_by=vo.UserId(id=input.created_by),
            check_permissions=lambda ps, id: self.security_port.check_permissions(
                ps, id.id)
        )

        return self.Output.from_entity(self.save_port.save_permission(Permission.create(command)))
