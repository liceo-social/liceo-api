from liceo.infra.domain.vo import Paged
from liceo.security.users.application.dtos import FilterUsersDTO, UserDTO
from liceo.security.users.domain.entities import User
from liceo.labs.poirot.core import sql, Repository
from ..application.repository import UsersRepository


class MemoryRepository(UsersRepository):
    def save_user(self, user: User) -> User:
        return user


class PoirotUsersRepository(UsersRepository, Repository):
    def _map_to_user_dto(self, row: dict) -> UserDTO:
        return UserDTO(
            id=row["id"],
            full_name=row["full_name"],
            username=row["username"]
        )

    def filter_users(self, filter: FilterUsersDTO) -> Paged[UserDTO]:
        sql = self.resolve_sql(self.filter_users)
        sql_params: dict = {
            "offset": filter.pagination.get_offset(),
            "max": filter.pagination.max
        }

        if (filter.name is not None):
            sql_params.update({"name": f"%{filter.name}%"})

        result = self._get_connection().all(
            sql, params=sql_params, order_by={"name": False})
        data = list(map(self._map_to_user_dto, result))
        total_count = result[0]["total_count"]

        return Paged(total=0 if len(result) == 0 else total_count, data=data)

    def save_user(self, user: User) -> User:
        sql = self.resolve_sql(self.save_user)
        self._get_connection().insert(sql, params={
            "id": user.id.id,
            "name": user.name,
            "surname": user.surname,
            "username": user.username,
            "password": user.password,
            "created_at": user.created_at,
            "created_by": user.created_by.id
        })
        self._save_user_roles(user)
        return user

    def _save_user_roles(self, user: User) -> User:
        user_sql = self.resolve_sql(self._save_user_roles)

        for role in user.roles:
            role_id = self.find_role_id_by_name(role.name)
            if (role_id):
                self._get_connection().insert(user_sql, params={
                    "user_id": user.id.id,
                    "role_id": role_id
                })

        return user

    @sql(lambda row: row["id"] if row else None)
    def find_role_id_by_name(self, name: str) -> str | None:
        pass
