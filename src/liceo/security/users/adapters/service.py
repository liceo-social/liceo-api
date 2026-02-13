from dataclasses import dataclass
from liceo.infra.domain.vo import Paged
from liceo.infra.application.output import EventStore
from liceo.labs.db.core import managed_service, transactional, AbstractService, skip_default_connection
from liceo.security.common.application.service import SecurityService
from liceo.mail.application.service import MailScheduler, TemplateRenderer
from liceo.mail.application.dtos import QueueMailDTO

from . import mappers
from ..domain import vo, entities
from ..application import dtos, repository, service


@dataclass
@managed_service
class SendActivationMailService(service.UserNotificationService, AbstractService):
    mails: MailScheduler
    templates: TemplateRenderer

    @skip_default_connection
    @transactional()
    def send_activation_message(self, user: entities.User) -> entities.User:
        email_body = self.templates.render("users_activation.html", {
            "name": user.name,
            "username": user.username
        })
        self.mails.queue_mail(
            QueueMailDTO(
                recipient=user.username,
                subject="Activation",
                body=email_body,
                created_by=user.created_by.id
            )
        )
        return user


@dataclass
@managed_service
class UsersService(service.AbstractUsersService):
    users: repository.UsersRepository
    images: repository.UsersImagesRepository
    security: SecurityService
    event_store: EventStore
    notifications: service.UserNotificationService

    def get_user(self, input: dtos.GetUserDTO) -> dtos.UserDTO | None:
        return mappers.user_to_user_dto(self.users.find_user_by_id(input.id))

    def list(self, input: dtos.FilterUsersDTO) -> Paged[dtos.UserDTO]:
        return self.users.filter_users(input)

    def _save_user_photo(self, user: entities.User) -> None:
        if user.photo:
            self.images.save_user_image(
                dtos.SaveUserImageDTO(
                    user_id=user.id.id,
                    photo_id=user.photo,
                    dimension="original",
                    created_by=user.created_by.id,
                    created_at=user.created_at
                )
            )

    @transactional()
    def create_user(self, input: dtos.CreateUserDTO) -> entities.User:
        command = entities.User.CreateUserCommand(
            next_id=self.users.generate_id,
            created_by_admin=input.created_by.is_admin,
            name=input.name,
            photo=input.photo,
            surname=input.surname,
            username=input.username,
            role=input.role,
            created_by=vo.UserId(id=input.created_by.id)
        )
        saved_user = self.users.save_user(entities.User.create(command))
        self._save_user_photo(saved_user)
        self.event_store.append(saved_user)
        self.notifications.send_activation_message(saved_user)
        return saved_user

    @transactional()
    def update_user(self, input: dtos.UpdateUserDetailsDTO) -> entities.User | None:
        loaded = self.users.find_user_by_id(input.id)

        if not loaded:
            return

        updated = loaded.update_details(entities.User.UpdateDetailsCommand(
            name=input.name,
            surname=input.surname,
            username=input.username,
            role=input.role,
            photo=input.photo,
            changed_by=vo.UserId(id=input.updated_by.id),
            changed_by_admin=input.updated_by.is_admin
        ))
        # saving user
        saved_user = self.users.update_user(updated)
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
    def update_password(self, input: dtos.UpdatePasswordDTO) -> entities.User | None:
        loaded = self.users.find_user_by_id(input.id)

        if not loaded:
            return

        # updating password
        updated = loaded.change_password(entities.User.ChangePasswordCommand(
            old_password=input.old_password,
            old_password_check_handler=lambda old_plain: self._check_old_passwd(
                old_plain, loaded.password),
            new_password=input.new_password,
            new_password_repeated=input.new_password_repeated,
            new_password_hashing_handler=self.security.hash_passw,
            changed_by=vo.UserId(id=input.updated_by.id)
        ))
        # persisting changes
        saved_user = self.users.update_password(updated)
        # saving audit trail
        self.event_store.append(saved_user)
        # return saved user
        return saved_user

    @transactional()
    def update_security(self, input: dtos.UpdateSecurityDTO) -> dtos.UpdatedSecurityDTO | None:
        loaded = self.users.find_user_by_id(input.id)

        if not loaded:
            return

        # updating user
        updated = loaded.update_security(
            entities.User.UpdateSecurityCommand(
                password_expired=input.password_expired,
                account_active=input.account_active,
                account_blocked=input.account_blocked,
                account_expired=input.account_expired,
                updated_by=vo.UserId(id=input.id),
                updated_by_admin=input.updated_by.is_admin
            )
        )
        # persisting changes
        saved_user = self.users.update_security(updated)
        # saving audit trail
        self.event_store.append(saved_user)
        # return saved_user
        return dtos.UpdatedSecurityDTO(
            password_expired=saved_user.password_expired,
            account_active=saved_user.account_active,
            account_blocked=saved_user.account_blocked,
            account_expired=saved_user.account_expired
        )
