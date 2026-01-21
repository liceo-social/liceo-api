from liceo.security.users.domain.entities import User
from liceo.security.users.domain.vo import UserId, Role
from liceo.security.users.domain.errors import (
    NotChangedBySameUserError, RepeatedPasswordNotCorrect, RoleAddedByNoAdmin, RoleRemovedByNoAdmin)


def create_user(user_id: UserId = UserId(id="1")):
    return User.create(User.CreateUserCommand(
        next_id=lambda: "user-id",
        created_by=user_id,
        name="Johnny",
        surname="Doe",
        username="john.doe@optiak.com",
        password="password",
    ))


def test_change_name():
    user_id = UserId("user-id")
    user = create_user(user_id=user_id)
    change_name_cmd = User.ChangeNameCommand(name="Johnny", changed_by=user_id)
    user = user.change_name(change_name_cmd)

    assert user.name == "Johnny"
    assert len(user._events) == 2


def test_try_to_change_name_by_another_user():
    user = create_user()
    change_name_cmd = User.ChangeNameCommand(
        name="Johnny", changed_by=UserId(id="another-user-id")
    )

    try:
        user.change_name(change_name_cmd)
        assert False
    except NotChangedBySameUserError:
        assert True

    assert user.name == "Johnny"
    assert len(user._events) == 1


def test_change_password():
    user_id = UserId(id="user-id")
    old_password = "old-password"
    new_password = "new_password"

    cmd = User.ChangePasswordCommand(
        old_password=old_password,
        old_password_check_handler=lambda pwd: True,
        new_password=new_password,
        new_password_repeated=new_password,
        new_password_hashing_handler=lambda pwd: "hashed",
        changed_by=user_id,
    )
    user = create_user(user_id=user_id).change_password(cmd)

    assert len(user._events) == 2
    assert user.password == "hashed"


def test_try_to_change_password_with_wrong_repeated_password():
    user_id = UserId(id="user-id")
    user = create_user(user_id=user_id)
    try:
        cmd = User.ChangePasswordCommand(
            old_password="password",
            old_password_check_handler=lambda pwd: pwd == user.password,
            new_password="new-password",
            new_password_repeated="wrong-new-password",
            new_password_hashing_handler=lambda pwd: "hashed",
            changed_by=user_id,
        )
        user.change_password(cmd)
        assert False
    except RepeatedPasswordNotCorrect:
        assert True

    assert len(user._events) == 1
    assert user.password == "password"


def test_try_to_change_password_by_another_user():
    user_id = UserId(id="user-id")

    user = create_user(user_id=user_id)
    try:
        cmd = User.ChangePasswordCommand(
            old_password="password",
            old_password_check_handler=lambda pwd: pwd == user.password,
            new_password="new-password",
            new_password_repeated="new-password",
            new_password_hashing_handler=lambda pwd: "hashed",
            changed_by=UserId("another-user-id"),
        )
        user.change_password(cmd)
        assert False
    except NotChangedBySameUserError:
        assert True

    assert len(user._events) == 1
    assert user.password == "password"


def add_role_cmd_by_admin():
    return User.AddRoleCommand(
        added_by=UserId(id="admin-id"),
        role_to_add=Role.ROLE_USER,
        admin_check_handler=lambda user: True,
    )


def test_add_role():
    user = create_user()
    user = user.add_role(add_role_cmd_by_admin())
    assert len(user.roles) == 1
    assert user.roles[0] == Role.ROLE_USER


def test_non_admin_user_adding_a_role_to_user():
    no_admin_id = UserId(id="no-admin-id")
    user = create_user()
    try:
        user.add_role(
            User.AddRoleCommand(
                added_by=no_admin_id,
                role_to_add=Role.ROLE_USER,
                admin_check_handler=lambda user: False,
            )
        )
        assert False
    except RoleAddedByNoAdmin:
        assert True

    assert len(user._events) == 1
    assert len(user.roles) == 0


def test_adding_same_role_more_than_once():
    user = create_user()
    assert len(user._events) == 1
    assert len(user.roles) == 0

    user.add_role(add_role_cmd_by_admin()).add_role(add_role_cmd_by_admin())
    assert len(user._events) == 2
    assert len(user.roles) == 1


def remove_cmd_by(is_admin: bool = True):
    return User.RemoveRoleCommand(
        removed_by=UserId("admin-id"),
        role_to_delete=Role.ROLE_USER,
        admin_check_handler=lambda user: is_admin,
    )


def test_removing_role():
    user = create_user()
    assert len(user._events) == 1
    assert len(user.roles) == 0

    user.add_role(add_role_cmd_by_admin())
    assert len(user._events) == 2
    assert len(user.roles) == 1

    user.remove_role(remove_cmd_by())
    assert len(user._events) == 3
    assert len(user.roles) == 0


def test_trying_to_remove_a_role_by_a_non_admin_user():
    user = create_user()
    assert len(user._events) == 1
    assert len(user.roles) == 0

    user.add_role(add_role_cmd_by_admin())
    assert len(user._events) == 2
    assert len(user.roles) == 1

    try:
        user.remove_role(remove_cmd_by(is_admin=False))
        assert False
    except RoleRemovedByNoAdmin:
        assert True

    assert len(user._events) == 2
    assert len(user.roles) == 1


def test_removing_an_already_removed_role():
    user = create_user()
    assert len(user._events) == 1
    assert len(user.roles) == 0

    user.add_role(add_role_cmd_by_admin())
    assert len(user._events) == 2
    assert len(user.roles) == 1

    user.remove_role(remove_cmd_by())
    assert len(user._events) == 3
    assert len(user.roles) == 0

    user.remove_role(remove_cmd_by())
    assert len(user._events) == 3
    assert len(user.roles) == 0
