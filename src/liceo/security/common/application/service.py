from .cases import HashPassword, CheckUserPermissions


class SecurityService(HashPassword, CheckUserPermissions):
    def hash_passw(self, pwd) -> str:
        return super().hash_passw(pwd)

    def check_permissions(self, permissions: list[str], user_id: str) -> bool:
        return super().check_permissions(permissions, user_id)
