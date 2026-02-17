import pytest
from liceo.security.authentication.domain.entities import User
from liceo.security.authentication.domain.vo import UserId
from liceo.security.common.domain.errors import AuthenticationException

TOKEN = "token"


def create_user():
    user = User(id=UserId(id="user-id"))
    user.username = "user@liceo.social"
    user.roles = ["ROLE_ADMIN"]
    return user


def TOKEN_GENERATOR(username: str, roles: list[str]):
    return TOKEN


def test_should_authenticate_successfully_with_proper_credentials():
    command = User.AuthenticationCommand(
        username="username@domain.com",
        password="password",
        password_matches=True,
        token_generator=TOKEN_GENERATOR
    )

    authenticated_user = create_user().authenticate(command)
    assert authenticated_user.token == TOKEN
    assert len(authenticated_user._events) == 1


def test_should_fail_when_missing_credentials():
    command = User.AuthenticationCommand(
        username="",
        password="",
        password_matches=True,
        token_generator=TOKEN_GENERATOR
    )

    with pytest.raises(AuthenticationException):
        create_user().authenticate(command)


def test_should_fail_when_credentials_are_empty():
    command = User.AuthenticationCommand(
        username="",
        password="",
        password_matches=True,
        token_generator=TOKEN_GENERATOR
    )

    with pytest.raises(AuthenticationException):
        create_user().authenticate(command)


def test_should_fail_when_username_is_not_long_enough():
    command = User.AuthenticationCommand(
        username="some",
        password="password",
        password_matches=True,
        token_generator=TOKEN_GENERATOR
    )

    with pytest.raises(AuthenticationException):
        create_user().authenticate(command)


def test_should_fail_when_password_is_not_long_enough():
    command = User.AuthenticationCommand(
        username="some",
        password="pass",
        password_matches=True,
        token_generator=TOKEN_GENERATOR
    )

    with pytest.raises(AuthenticationException):
        create_user().authenticate(command)
