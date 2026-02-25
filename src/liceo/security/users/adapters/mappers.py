from ..domain.entities import User
from ..application.dtos import UserDTO


def map_to_user_dto(row: dict) -> UserDTO:
    return UserDTO(
        id=row["id"],
        version=row["version"],
        name=row["name"],
        surname=row["surname"],
        full_name=row["full_name"],
        photo=row["photo"],
        username=row["username"],
        roles=row["roles"],
        created_by=row.get("created_by", ""),
        password_expired=row["password_expired"],
        account_active=row["account_active"],
        account_blocked=row["account_blocked"],
        account_expired=row["account_expired"]
    )


def user_to_user_dto(user: User | None) -> UserDTO | None:
    if not user:
        return None

    return UserDTO(
        id=user.id.id,
        version=user._version,
        name=user.name,
        surname=user.surname,
        full_name=user.full_name,
        photo=user.photo,
        username=user.username,
        roles=user.roles,
        created_by=user.created_by.id,
        password_expired=user.password_expired,
        account_active=user.account_active,
        account_blocked=user.account_blocked,
        account_expired=user.account_expired,
    )
