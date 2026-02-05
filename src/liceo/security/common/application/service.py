import jwt
import bcrypt
from dataclasses import dataclass
from liceo.infra.adapters.di import LiceoConfiguration
from .cases import HashPassword, CheckPermissions, GenerateToken
from .repositories import PermissionsRepository


@dataclass
class SecurityService(HashPassword, CheckPermissions, GenerateToken):
    config: LiceoConfiguration
    repository: PermissionsRepository

    def hash_passw(self, pwd) -> str:
        return bcrypt.hashpw(pwd.encode(), self.config.crypto.salt.encode()).decode()

    def verify(self, password: str, hashed: str) -> bool:
        password_bytes = password.encode()
        hashed_bytes = hashed.encode()
        return bcrypt.checkpw(password=password_bytes, hashed_password=hashed_bytes)

    def check_permission_in_roles(self, permission: str, roles: list[str]) -> bool:
        found_roles = self.repository.find_all_roles_by_permission_name(permission)
        return any(x in roles for x in found_roles)

    def generate_token(self, username: str, roles: list[str]) -> str:
        payload = {
            "sub": username,
            "roles": roles
        }

        return jwt.encode(
            payload,
            self.config.crypto.secret_key,
            algorithm=self.config.crypto.algorithm
        )

    def decode_token(self, token: str) -> dict:
        payload = jwt.decode(
            token,
            key=self.config.crypto.secret_key,
            algorithms=[self.config.crypto.algorithm]
        )

        return {
            "username": payload.get("sub"),
            "roles": payload.get("roles")
        }
