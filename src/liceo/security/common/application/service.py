from dataclasses import dataclass
from liceo.infra.adapters.di import LiceoConfiguration
from .cases import HashPassword, CheckUserPermissions, GenerateToken
import bcrypt
import jwt


@dataclass
class SecurityService(HashPassword, CheckUserPermissions, GenerateToken):
    config: LiceoConfiguration

    def hash_passw(self, pwd) -> str:
        return bcrypt.hashpw(pwd.encode(), self.config.crypto.salt.encode()).decode()

    def check_permissions(self, permissions: list[str], user_id: str) -> bool:
        return True

    def generate_token(self, username: str) -> str:
        to_encode = {"sub": username}
        return jwt.encode(
            to_encode,
            self.config.crypto.secret_key,
            algorithm=self.config.crypto.algorithm
        )
