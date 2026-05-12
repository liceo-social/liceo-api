from pydantic import BaseModel, Field
from liceo.infra.domain.vo import Pagination
from liceo.security.common.adapters.di import UserInfo
from liceo.security.common.application.dto import CurrentUserDTO
from ..application.dtos import CreateUserDTO, FilterUsersDTO, UpdateUserDetailsDTO, UpdatePasswordDTO, UpdateSecurityDTO, GetUserDTO, SendResetPasswordEmailDTO, ConfirmResetPasswordDTO


class UserDetails(BaseModel):
    name: str
    surname: str
    photo: str | None = None
    username: str
    role: str


class CreateUserRequest(BaseModel):
    fields: UserDetails
    created_by: UserInfo

    def to_input(self) -> CreateUserDTO:
        return CreateUserDTO(
            name=self.fields.name,
            surname=self.fields.surname,
            username=self.fields.username,
            photo=self.fields.photo,
            role=self.fields.role,
            created_by=CurrentUserDTO(
                id=self.created_by.id,
                roles=self.created_by.roles,
                is_admin=self.created_by.is_admin
            )
        )


class UpdateUserDetails(UserDetails):
    version: int


class UpdateUserRequest(BaseModel):
    id: str
    fields: UpdateUserDetails
    updated_by: UserInfo

    def to_input(self) -> UpdateUserDetailsDTO:
        return UpdateUserDetailsDTO(
            id=self.id,
            version=self.fields.version,
            name=self.fields.name,
            surname=self.fields.surname,
            username=self.fields.username,
            photo=self.fields.photo,
            role=self.fields.role,
            updated_by=CurrentUserDTO(
                id=self.updated_by.id,
                roles=self.updated_by.roles,
                is_admin=self.updated_by.is_admin
            )
        )


class FilteringUsersRequest(BaseModel):
    max: int = Field(100, gt=0, le=100)
    page: int = Field(0, ge=0)
    name: str | None = None
    surname: str | None = None
    username: str | None = None

    def to_pagination(self):
        return Pagination(self.max, self.page)

    def toDTO(self):
        return FilterUsersDTO(
            name=self.name,
            surname=self.surname,
            username=self.username,
            pagination=self.to_pagination()
        )


class UpdatePasswordFields(BaseModel):
    version: int
    old_password: str
    new_password: str
    new_password_repeated: str


class UpdatePasswordRequest(BaseModel):
    id: str
    fields: UpdatePasswordFields
    updated_by: UserInfo

    def to_input(self) -> UpdatePasswordDTO:
        return UpdatePasswordDTO(
            id=self.id,
            version=self.fields.version,
            old_password=self.fields.old_password,
            new_password=self.fields.new_password,
            new_password_repeated=self.fields.new_password_repeated,
            updated_by=CurrentUserDTO(
                id=self.updated_by.id,
                roles=self.updated_by.roles,
                is_admin=self.updated_by.is_admin
            )
        )


class UpdateSecurityFields(BaseModel):
    version: int
    password_expired: bool
    account_active: bool
    account_blocked: bool
    account_expired: bool


class UpdateSecurityRequest(BaseModel):
    id: str
    fields: UpdateSecurityFields
    updated_by: UserInfo

    def to_input(self) -> UpdateSecurityDTO:
        return UpdateSecurityDTO(
            id=self.id,
            version=self.fields.version,
            account_active=self.fields.account_active,
            account_blocked=self.fields.account_blocked,
            account_expired=self.fields.account_expired,
            password_expired=self.fields.password_expired,
            updated_by=CurrentUserDTO(
                id=self.updated_by.id,
                roles=self.updated_by.roles,
                is_admin=self.updated_by.is_admin
            )
        )


class ShowUserRequest(BaseModel):
    id: str

    def to_dto(self) -> GetUserDTO:
        return GetUserDTO(self.id)


class ResetPasswordRequest(BaseModel):
    username: str

    def to_dto(self) -> SendResetPasswordEmailDTO:
        return SendResetPasswordEmailDTO(self.username)


class ResetPasswordConfirmationRequest(BaseModel):
    token: str
    username: str
    password: str
    password_repeated: str

    def to_dto(self) -> ConfirmResetPasswordDTO:
        return ConfirmResetPasswordDTO(token=self.token, password=self.password, password_repeated=self.password_repeated, username=self.username)
