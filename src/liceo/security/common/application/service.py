import jwt
import bcrypt
from dataclasses import dataclass
from liceo.infra.domain.vo import LiceoConfiguration
from liceo.labs.db.core import ConnectionManagerFactory, managed_service
from .cases import HashPassword, CheckPermissions, GenerateToken
from .repositories import PermissionsRepository


@dataclass
@managed_service
class SecurityService(HashPassword, CheckPermissions, GenerateToken):
    config: LiceoConfiguration
    repository: PermissionsRepository
    connection_manager_factory: ConnectionManagerFactory

    def hash_passw(self, pwd) -> str:
        return bcrypt.hashpw(pwd.encode(), self.config.crypto.salt.encode()).decode()

    def verify(self, password: str, hashed: str) -> bool:
        password_bytes = password.encode()
        hashed_bytes = hashed.encode()
        return bcrypt.checkpw(password=password_bytes, hashed_password=hashed_bytes)

    def check_permission_in_roles(self, permission: str, roles: list[str]) -> bool:
        found_roles = self.repository.find_all_roles_by_permission_name(permission)
        return any(x in roles for x in found_roles)

    def generate_token(self, id: str, roles: list[str]) -> str:
        payload = {
            "sub": id,
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
            "sub": payload.get("sub"),
            "roles": payload.get("roles")
        }
