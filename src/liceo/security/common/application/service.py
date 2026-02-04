from dataclasses import dataclass
from liceo.infra.adapters.di import LiceoConfiguration
from .cases import HashPassword, CheckUserPermissions
import bcrypt


@dataclass
class SecurityService(HashPassword, CheckUserPermissions):
    config: LiceoConfiguration

    def hash_passw(self, pwd) -> str:
        return bcrypt.hashpw(pwd.encode(), self.config.crypto.salt.encode()).decode()

    def check_permissions(self, permissions: list[str], user_id: str) -> bool:
        return True
