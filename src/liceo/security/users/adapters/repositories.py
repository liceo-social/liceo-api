from liceo.security.users.domain.entities import User
from liceo.labs.poirot.core import sql, Repository
from ..application.ports import SaveUserPort


class MemoryRepository(SaveUserPort):
    def save_user(self, user: User) -> User:
        return user


class UserRepository(SaveUserPort, Repository):
    @sql()
    def save_user(self, user: User) -> User:
        sql = self.resolve_sql(self.save_user)
        self.connection.insert(sql, params={
            "id": user.id,
            "name": user.name,
            "surname": user.surname,
            "username": user.username,
            "password": user.password
        })
        self._save_user_roles(user)
        return user

    @sql()
    def _save_user_roles(self, user: User) -> User:
        user_sql = self.resolve_sql(self._save_user_roles)

        for role in user.roles:
            role_id = self._find_role_id_by_name(role.value)
            if (role_id):
                self.connection.insert(user_sql, params={
                    "user_id": user.id,
                    "role_id": role_id
                })

        return user

    @sql()
    def _find_role_id_by_name(self, name: str) -> str | None:
        pass
