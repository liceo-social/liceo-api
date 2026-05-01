from datetime import datetime, timedelta
from liceo.infra.domain.vo import Paged, AuditInfo
from liceo.security.users.application.dtos import FilterUsersDTO, UserDTO, UpsertUserImageDTO
from liceo.security.users.domain.entities import User
from liceo.labs.db.sql import SQLRepository, sql
from ..application.repository import UsersRepository, UsersImagesRepository, UsersOneTimeTokensRepository
from ..domain.vo import UserId
from . import mappers


class SQLUsersRepository(UsersRepository, SQLRepository):
    @staticmethod
    def _map_to_user(row: dict) -> User:
        user = User(
            id=UserId(id=row["id"])
        )
        user.audit = AuditInfo(created_by=UserId(id=row["created_by"]))
        user.name = row["name"]
        user._version = row["version"]
        user.surname = row["surname"]
        user.password = row["password"]
        user.photo = row["photo"]
        user.username = row["username"]
        user.roles = row["roles"]
        user.password_expired = row["password_expired"]
        user.account_active = row["account_active"]
        user.account_blocked = row["account_blocked"]
        user.account_expired = row["account_expired"]
        return user

    @sql(_map_to_user)
    def find_user_by_id(self, id: str) -> User | None:
        return None

    @sql(_map_to_user)
    def find_user_by_token_and_username(self, token: str, username: str) -> User | None:
        return None

    @sql(_map_to_user)
    def find_user_by_username(self, username: str) -> User | None:
        return None

    def filter_users(self, filter: FilterUsersDTO) -> Paged[UserDTO]:
        sql = self.resolve_sql(self.filter_users)
        params: dict = {
            "offset": filter.pagination.get_offset(),
            "max": filter.pagination.max
        }

        if (filter.name is not None):
            params.update({"name": f"%{filter.name}%"})

        sql = self.sql_optimize(sql, params, {"created_at": False})
        result = self._get_connection().all(
            sql,
            params=params
        )
        data = list(map(mappers.map_to_user_dto, result))
        total_count = result[0]["total_count"]

        return Paged(total=0 if len(result) == 0 else total_count, data=data)

    def save_user(self, user: User) -> User:
        sql = self.resolve_sql(self.save_user)
        self._get_connection().insert(sql, params={
            "id": user.id.id,
            "version": user._version,
            "name": user.name,
            "surname": user.surname,
            "username": user.username,
            "created_at": user.created_at,
            "created_by": user.created_by.id,
            "last_updated_at": user.last_updated_at,
            "last_updated_by": user.last_updated_by
        })
        self._save_user_roles(user)
        return user

    @sql(lambda row: row["id"] if row else None)
    def find_role_id_by_name(self, name: str) -> str | None:
        pass

    def _save_user_roles(self, user: User) -> User:
        user_sql = self.resolve_sql(self._save_user_roles)

        for role in user.roles:
            role_id = self.find_role_id_by_name(role)
            if (role_id):
                self._get_connection().insert(user_sql, params={
                    "user_id": user.id.id,
                    "role_id": role_id
                })

        return user

    @sql()
    def _delete_all_roles_by_user_id(self, id: str) -> None:
        pass

    def _update_user_roles(self, user: User) -> User:
        # deleting previous roles
        self._get_connection().execute(
            self.resolve_sql(self._delete_all_roles_by_user_id),
            params={"id": user.id.id}
        )
        # adding new
        return self._save_user_roles(user)

    def update_user(self, user: User) -> User:
        sql = self.resolve_sql(self.update_user)
        self._get_connection().execute(sql, params={
            "id": user.id.id,
            "version": user._version,
            "name": user.name,
            "surname": user.surname,
            "username": user.username,
            "last_updated_at": user.last_updated_at,
            "last_updated_by": user.last_updated_by
        })
        return self._update_user_roles(user)

    def update_password(self, user: User) -> User:
        sql = self.resolve_sql(self.update_password)
        self._get_connection().execute(sql, params={
            "id": user.id.id,
            "version": user._version,
            "password": user.password,
            "last_updated_at": user.last_updated_at,
            "last_updated_by": user.last_updated_by.id
        })
        return user

    def update_security(self, user: User) -> User:
        sql = self.resolve_sql(self.update_security)
        self._get_connection().execute(sql, params={
            "id": user.id.id,
            "version": user._version,
            "password_expired": user.password_expired,
            "account_active": user.account_active,
            "account_blocked": user.account_blocked,
            "account_expired": user.account_expired,
            "last_updated_at": user.last_updated_at,
            "last_updated_by": user.last_updated_by
        })
        return user


class SQLUsersImagesRepository(UsersImagesRepository, SQLRepository):
    def save_user_image(self, dto: UpsertUserImageDTO) -> None:
        sql = self.resolve_sql(self.save_user_image)
        params = params = {
            "user_id": dto.user_id,
            "storage_id": dto.photo_id,
            "dimension": dto.dimension,
            "created_at": dto.created_at,
            "created_by": dto.created_by,
            "last_updated_by": dto.last_updated_by,
            "last_updated_at": dto.last_updated_at
        }
        print(params)
        self._get_connection().execute(sql, params)


class SQLUsersOneTimeTokensRepository(UsersOneTimeTokensRepository, SQLRepository):
    @sql()
    def delete_all_tokens_by_user_id(self, user_id: str) -> None:
        return None

    def save_reset_hashed_token(self, user: User) -> None:
        sql = self.resolve_sql(self.save_reset_hashed_token)
        last_reset_token = user.reset_password_token

        if not last_reset_token:
            return

        self._get_connection().execute(
            sql,
            params={
                "id": self.generate_id(),
                "user_id": user.id.id,
                "token_hash": last_reset_token.hashed_token,
                "created_at": last_reset_token.created_at,
                "expires_at": last_reset_token.expires_at
            }
        )
