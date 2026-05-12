from pydantic import BaseModel
from liceo.infra.domain.vo import Paged
from ..domain.entities import User
from ..application.dtos import UpdatedSecurityDTO
from ..application.dtos import UserDTO


class CreateUserResponse(BaseModel):
    id: str

    @staticmethod
    def from_user(user: User):
        return CreateUserResponse(id=user.id.id)


class UpdateUserDetailsResponse(BaseModel):
    id: str
    version: int
    name: str
    surname: str
    photo: str | None = None
    username: str
    role: str

    @staticmethod
    def from_user(user: User | None):
        if (user):
            return UpdateUserDetailsResponse(
                id=user.id.id,
                version=user._version,
                name=user.name,
                surname=user.surname,
                photo=user.photo,
                username=user.username,
                role=user.roles[0]
            )


class UpdatePasswordResponse(BaseModel):
    id: str
    version: int

    @staticmethod
    def from_user(user: User | None):
        if (user):
            return UpdatePasswordResponse(id=user.id.id, version=user._version)


class ListUsersResponse(BaseModel):
    data: list[UserDTO]
    total_count: int

    @staticmethod
    def from_dto(dto: Paged[UserDTO]):
        return ListUsersResponse(data=dto.data, total_count=dto.total)


class UpdatedSecurityResponse(BaseModel):
    id: str
    version: int
    password_expired: bool
    account_active: bool
    account_blocked: bool
    account_expired: bool

    @staticmethod
    def from_dto(dto: UpdatedSecurityDTO | None):
        if not dto:
            return None
        return UpdatedSecurityResponse(
            id=dto.id,
            version=dto.version,
            password_expired=dto.password_expired,
            account_active=dto.account_active,
            account_blocked=dto.account_blocked,
            account_expired=dto.account_expired
        )


class ShowUserResponse(BaseModel):
    id: str
    version: int
    name: str
    surname: str
    username: str
    photo: str | None
    role: str
    password_expired: bool
    account_active: bool
    account_blocked: bool
    account_expired: bool
    created_by: str

    @staticmethod
    def from_dto(dto: UserDTO | None):
        if not dto:
            return None
        return ShowUserResponse(
            id=dto.id,
            version=dto.version,
            name=dto.name,
            surname=dto.surname,
            username=dto.username,
            photo=dto.photo,
            role=dto.roles[0],
            account_active=dto.account_active,
            password_expired=dto.password_expired,
            account_blocked=dto.account_blocked,
            account_expired=dto.account_expired,
            created_by=dto.created_by,
        )


class ResetPasswordRequestResponse(BaseModel):
    result: str = "ok"


class ResetPasswordConfirmationResponse(BaseModel):
    pass

    @staticmethod
    def from_confirmation(confirmation: None) -> "ResetPasswordConfirmationResponse":
        return ResetPasswordConfirmationResponse()
