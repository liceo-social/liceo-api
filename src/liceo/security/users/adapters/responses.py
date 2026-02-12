from pydantic import BaseModel
from liceo.infra.domain.vo import Paged
from ..domain.entities import User
from ..application.dtos import UpdatedSecurityDTO
from .repositories import UserDTO


class CreateUserResponse(BaseModel):
    id: str

    @staticmethod
    def from_user(user: User):
        return CreateUserResponse(id=user.id.id)


class UpdateUserResponse(BaseModel):
    id: str

    @staticmethod
    def from_user(user: User | None):
        if (user):
            return UpdateUserResponse(id=user.id.id)


class UpdatePasswordResponse(BaseModel):
    id: str

    @staticmethod
    def from_user(user: User | None):
        if (user):
            return UpdatePasswordResponse(id=user.id.id)


class ListUsersResponse(BaseModel):
    data: list[UserDTO]
    total_count: int

    @staticmethod
    def from_dto(dto: Paged[UserDTO]):
        return ListUsersResponse(data=dto.data, total_count=dto.total)


class UpdatedSecurityResponse(BaseModel):
    password_expired: bool
    account_active: bool
    account_blocked: bool
    account_expired: bool

    @staticmethod
    def from_dto(dto: UpdatedSecurityDTO | None):
        if not dto:
            return None
        return UpdatedSecurityResponse(
            password_expired=dto.password_expired,
            account_active=dto.account_active,
            account_blocked=dto.account_blocked,
            account_expired=dto.account_expired
        )
