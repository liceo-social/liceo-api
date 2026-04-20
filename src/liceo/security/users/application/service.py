from abc import abstractmethod, ABC
from liceo.infra.domain.vo import Paged
from ..domain.entities import User
from . import dtos


class AbstractUsersService(ABC):
    @abstractmethod
    def get_user(self, input: dtos.GetUserDTO) -> dtos.UserDTO | None:
        pass

    @abstractmethod
    def list(self, input: dtos.FilterUsersDTO) -> Paged[dtos.UserDTO]:
        pass

    @abstractmethod
    def create_user(self, input: dtos.CreateUserDTO) -> User:
        pass

    @abstractmethod
    def update_user(self, input: dtos.UpdateUserDetailsDTO) -> User | None:
        pass

    @abstractmethod
    def update_password(self, input: dtos.UpdatePasswordDTO) -> User | None:
        pass

    @abstractmethod
    def update_security(self, input: dtos.UpdateSecurityDTO) -> dtos.UpdatedSecurityDTO | None:
        pass

    @abstractmethod
    def send_reset_password_email(self, input: dtos.SendResetPasswordEmailDTO):
        pass

    @abstractmethod
    def confirm_reset_password(self, input: dtos.ConfirmResetPasswordDTO):
        pass


class UserNotificationService(ABC):
    @abstractmethod
    def send_activation_message(self, user: User) -> User:
        pass

    @abstractmethod
    def send_reset_password_message(self, dto: dtos.SendResetPasswordMessageByMailDTO):
        pass
