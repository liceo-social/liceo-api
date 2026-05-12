from liceo.security.users.domain.entities import User
from liceo.security.users.domain.vo import UserId
from liceo.security.users.domain import errors

WRONG_VERSION = 999
def ALLOWED_PERMISSION_FN(permissions, user_id): return True


def create_user(user_id: UserId = UserId(id="1")):
    return User.create(User.CreateUserCommand(
        next_id=lambda: "user-id",
        created_by=user_id,
        name="Johnny",
        surname="Doe",
        photo=None,
        username="john.doe@liceo.social",
        role='ROLE_USER',
        created_by_admin=True
    ))


def test_change_details():
    user_id = UserId("user-id")
    user = create_user(user_id=user_id)
    change_name_cmd = User.UpdateDetailsCommand(
        expected_version=user._version,
        name="Johnny",
        surname="Doe",
        username="johnny.be@bad.com",
        role="ROLE_USER",
        photo=None,
        changed_by_admin=False,
        changed_by=user_id,
    )
    user = user.update_details(change_name_cmd)

    assert user.name == "Johnny"
    assert len(user._events) == 2


def test_try_to_change_name_concurrently():
    user = create_user()
    change_name_cmd = User.UpdateDetailsCommand(
        expected_version=WRONG_VERSION,
        name="Johnny",
        surname="Doe",
        username="johnny.be@bad.com",
        role="ROLE_USER",
        photo=None,
        changed_by_admin=False,
        changed_by=UserId(id="another-user-id")
    )

    try:
        user.update_details(change_name_cmd)
        assert False
    except errors.EditedByOtherUser:
        assert True

    assert user.name == "Johnny"
    assert len(user._events) == 1


def test_try_to_change_name_by_another_user():
    user = create_user()
    change_name_cmd = User.UpdateDetailsCommand(
        expected_version=user._version,
        name="Johnny",
        surname="Doe",
        username="johnny.be@bad.com",
        role="ROLE_USER",
        photo=None,
        changed_by_admin=False,
        changed_by=UserId(id="another-user-id")
    )

    try:
        user.update_details(change_name_cmd)
        assert False
    except errors.NotChangedBySameUserError:
        assert True

    assert user.name == "Johnny"
    assert len(user._events) == 1


def test_change_password():
    user_id = UserId(id="user-id")
    old_password = "old-password"
    new_password = "new_password"

    user = create_user(user_id=user_id)
    cmd = User.ChangePasswordCommand(
        expected_version=user._version,
        old_password=old_password,
        old_password_check_handler=lambda pwd: True,
        new_password=new_password,
        new_password_repeated=new_password,
        new_password_hashing_handler=lambda pwd: "hashed",
        changed_by=user_id,
    )

    user.change_password(cmd)

    assert len(user._events) == 2
    assert user.password == "hashed"


def test_try_to_change_password_with_wrong_repeated_password():
    user_id = UserId(id="user-id")
    user = create_user(user_id=user_id)
    try:
        cmd = User.ChangePasswordCommand(
            expected_version=user._version,
            old_password=None,
            old_password_check_handler=lambda pwd: pwd == user.password,
            new_password="new-password",
            new_password_repeated="wrong-new-password",
            new_password_hashing_handler=lambda pwd: "hashed",
            changed_by=user_id,
        )
        user.change_password(cmd)
        assert False
    except errors.RepeatedPasswordNotCorrect:
        assert True

    assert len(user._events) == 1
    assert user.password is None


def test_try_to_change_password_by_another_user():
    user_id = UserId(id="user-id")

    user = create_user(user_id=user_id)
    try:
        cmd = User.ChangePasswordCommand(
            expected_version=user._version,
            old_password=None,
            old_password_check_handler=lambda pwd: pwd == user.password,
            new_password="new-password",
            new_password_repeated="new-password",
            new_password_hashing_handler=lambda pwd: "hashed",
            changed_by=UserId("another-user-id"),
        )
        user.change_password(cmd)
        assert False
    except errors.NotChangedBySameUserError:
        assert True

    assert len(user._events) == 1
    assert user.password is None


def test_try_to_change_password_by_wrong_old_password():
    user_id = UserId(id="user-id")

    user = create_user(user_id=user_id)
    try:
        cmd = User.ChangePasswordCommand(
            expected_version=user._version,
            old_password=None,
            old_password_check_handler=lambda pwd: False,
            new_password="new-password",
            new_password_repeated="new-password",
            new_password_hashing_handler=lambda pwd: "hashed",
            changed_by=user_id,
        )
        user.change_password(cmd)
        assert False
    except errors.OldPasswordNotCorrect:
        assert True

    assert len(user._events) == 1
    assert user.password is None


def test_try_to_change_password_concurrently():
    user_id = UserId(id="user-id")

    user = create_user(user_id=user_id)
    try:
        cmd = User.ChangePasswordCommand(
            expected_version=WRONG_VERSION,
            old_password=None,
            old_password_check_handler=lambda pwd: False,
            new_password="new-password",
            new_password_repeated="new-password",
            new_password_hashing_handler=lambda pwd: "hashed",
            changed_by=user_id,
        )
        user.change_password(cmd)
        assert False
    except errors.EditedByOtherUser:
        assert True

    assert len(user._events) == 1
    assert user.password is None
