from dataclasses import dataclass
from typing import List
from liceo.infra.domain.vo import Paged, Pagination
from liceo.labs.sherlock.application.service import EventStoreService
from liceo.labs.db.core import AbstractService, managed_service, transactional

from ..domain import entities, vo
from ..application import service, repository, dtos
from . import mappers


@dataclass
@managed_service
class DatabaseRolesService(service.RolesService, AbstractService):
    roles: repository.RolesRepository
    event_store: EventStoreService

    def show(self, dto: dtos.ShowRoleDTO) -> dtos.FullRoleDTO | None:
        role = self.roles.find_by_id(dto.id)

        if not role:
            return

        return mappers.map_role_to_full_role_dto(
            role,
            self.roles.find_all_permissions_by_role_id(role.id.id)
        )

    def list(self, pagination: Pagination) -> Paged[dtos.RoleDTO]:
        return self.roles.paged_roles(
            max=pagination.max,
            offset=pagination.get_offset()
        ).map(mappers.map_from_role_to_dto)

    @transactional()
    def create_role(self, dto: dtos.CreateRoleDTO) -> dtos.RoleDTO:
        created = entities.Role.create(entities.Role.CreateRoleCommand(
            next_id=self.roles.generate_id,
            is_admin=dto.is_admin,
            name=dto.name,
            description=dto.description,
            permissions=mappers.map_permissions(dto.permissions),
            created_by=vo.UserId(id=dto.created_by)
        ))
        saved = self.roles.save(created)
        self.roles.update_role_permissions(saved)
        self.event_store.append(saved)
        return mappers.map_from_role_to_dto(saved)

    @transactional()
    def update_role_details(self, dto: dtos.UpdateRoleDetailsDTO) -> entities.Role | None:
        loaded = self.roles.find_by_id(dto.id)

        if not loaded:
            return

        updated = loaded.modify_details(entities.Role.ChangeRoleDetailsCommand(
            name=dto.name,
            description=dto.description,
            expected_version=dto.version,
            is_admin=dto.is_admin,
            updated_by=vo.UserId(id=dto.updated_by)
        ))
        self.roles.update(updated)
        self.event_store.append(updated)
        return updated

    @transactional()
    def update_role_permissions(self, dto: dtos.UpdateRolePermissionsDTO) -> entities.Role | None:
        loaded = self.roles.find_by_id(dto.id)

        if not loaded:
            return

        updated = loaded.modify_permissions(
            entities.Role.ModifyPermissionsCommand(
                expected_version=dto.version,
                permissions=set([vo.PermissionId(id=p) for p in dto.permissions]),
                is_admin=dto.is_admin,
                changed_by=vo.UserId(id=dto.updated_by)
            )
        )
        self.roles.update_role_permissions(updated)
        self.event_store.append(updated)
        return loaded

    @transactional()
    def delete_role(self, dto: dtos.DeleteRoleDTO) -> None:
        loaded = self.roles.find_by_id(dto.id)

        if not loaded:
            return

        to_delete = loaded.delete(
            entities.Role.DeleteRoleCommand(
                expected_version=dto.version,
                is_admin=dto.is_admin,
                deleted_by=vo.UserId(id=dto.deleted_by)
            )
        )

        self.roles.delete(to_delete)
        self.event_store.append(to_delete)
