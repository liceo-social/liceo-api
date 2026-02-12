from dataclasses import dataclass
from liceo.security.common.application.service import SecurityService
from liceo.infra.application.output import EventStore
from liceo.labs.db.core import managed_service, transactional
from liceo.infra.domain.vo import Paged
from liceo.security.users.application.dtos import UpdatePasswordDTO, UpdateSecurityDTO, UpdateUserDetailsDTO, UpdatedSecurityDTO
from ..domain.entities import User
from ..domain.vo import UserId
from ..application.dtos import CreateUserDTO, FilterUsersDTO, UserDTO, SaveUserImageDTO
from ..application.repository import UsersRepository, UsersImagesRepository
from ..application.service import AbstractUsersService


@dataclass
@managed_service
class UsersService(AbstractUsersService):
    repository: UsersRepository
    images_repository: UsersImagesRepository
    security: SecurityService
    event_store: EventStore

    def list(self, input: FilterUsersDTO) -> Paged[UserDTO]:
        return self.repository.filter_users(input)

    def _save_user_photo(self, user: User) -> None:
        if user.photo:
            self.images_repository.save_user_image(
                SaveUserImageDTO(
                    user_id=user.id.id,
                    photo_id=user.photo,
                    dimension="original",
                    created_by=user.created_by.id,
                    created_at=user.created_at
                )
            )

    @transactional()
    def create_user(self, input: CreateUserDTO) -> User:
        command = User.CreateUserCommand(
            next_id=self.repository.generate_id,
            created_by_admin=input.created_by.is_admin,
            name=input.name,
            photo=input.photo,
            surname=input.surname,
            username=input.username,
            role=input.role,
            created_by=UserId(id=input.created_by.id)
        )
        # saving user
        saved_user = self.repository.save_user(User.create(command))
        # saving user photo
        if (saved_user.photo):
            self._save_user_photo(saved_user)
        # saving event trail
        self.event_store.append(saved_user)
        # return saved_user
        return saved_user

    @transactional()
    def update_user(self, input: UpdateUserDetailsDTO) -> User | None:
        loaded = self.repository.find_user_by_id(input.id)

        if not loaded:
            return

        updated = loaded.update_details(User.UpdateDetailsCommand(
            name=input.name,
            surname=input.surname,
            username=input.username,
            role=input.role,
            photo=input.photo,
            changed_by=UserId(id=input.updated_by.id),
            changed_by_admin=input.updated_by.is_admin
        ))
        # saving user
        saved_user = self.repository.update_user(updated)
        # saving user photo
        if (saved_user.photo):
            self._save_user_photo(saved_user)
        # saving event trail
        self.event_store.append(saved_user)
        # return saved_user
        return saved_user

    def _check_old_passwd(self, old_passwd_plain: str, old_passwd_hashed: str | None) -> bool:
        if not old_passwd_hashed:
            return False
        return self.security.verify(old_passwd_plain, old_passwd_hashed)

    @transactional()
    def update_password(self, input: UpdatePasswordDTO) -> User | None:
        loaded = self.repository.find_user_by_id(input.id)

        if not loaded:
            return

        # updating password
        updated = loaded.change_password(User.ChangePasswordCommand(
            old_password=input.old_password,
            old_password_check_handler=lambda old_plain: self._check_old_passwd(
                old_plain, loaded.password),
            new_password=input.new_password,
            new_password_repeated=input.new_password,
            new_password_hashing_handler=self.security.hash_passw,
            changed_by=UserId(id=input.updated_by.id)
        ))
        # persisting changes
        saved_user = self.repository.update_password(updated)
        # saving audit trail
        self.event_store.append(saved_user)
        # return saved user
        return saved_user

    @transactional()
    def update_security(self, input: UpdateSecurityDTO) -> UpdatedSecurityDTO | None:
        loaded = self.repository.find_user_by_id(input.id)

        if not loaded:
            return

        # updating user
        updated = loaded.update_security(
            User.UpdateSecurityCommand(
                password_expired=input.password_expired,
                account_active=input.account_active,
                account_blocked=input.account_blocked,
                account_expired=input.account_expired,
                updated_by=UserId(id=input.id),
                updated_by_admin=input.updated_by.is_admin
            )
        )
        # persisting changes
        saved_user = self.repository.update_security(updated)
        # saving audit trail
        self.event_store.append(saved_user)
        # return saved_user
        return UpdatedSecurityDTO(
            password_expired=saved_user.password_expired,
            account_active=saved_user.account_active,
            account_blocked=saved_user.account_blocked,
            account_expired=saved_user.account_expired
        )
