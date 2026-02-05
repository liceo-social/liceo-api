import pytest
from liceo.security.authentication.domain.entities import User
from liceo.security.authentication.domain.vo import UserId, UserAuthentication
from liceo.security.common.domain.errors import AuthenticationException

TOKEN = "token"


def AUTHENTICATION_SUCCESS(username, password):
    return UserAuthentication(id=UserId(id="1"), username="username", roles=["ROLE_ADMIN"], hashed="hashed")


def AUTHENTICATION_FAILS(username, password):
    return None


def TOKEN_GENERATOR(username: str, roles: list[str]):
    return TOKEN


def test_should_authenticate_successfully_with_proper_credentials():
    command = User.AuthenticationCommand(
        username="username@domain.com",
        password="password",
        authentication=AUTHENTICATION_SUCCESS,
        token_generator=TOKEN_GENERATOR
    )

    authenticated_user = User.authenticate(command)
    assert authenticated_user.token == TOKEN
    assert len(authenticated_user._events) == 1


def test_should_fail_when_missing_credentials():
    command = User.AuthenticationCommand(
        username="",
        password="",
        authentication=AUTHENTICATION_SUCCESS,
        token_generator=TOKEN_GENERATOR
    )

    with pytest.raises(AuthenticationException):
        User.authenticate(command)


def test_should_fail_when_credentials_are_empty():
    command = User.AuthenticationCommand(
        username="",
        password="",
        authentication=AUTHENTICATION_SUCCESS,
        token_generator=TOKEN_GENERATOR
    )

    with pytest.raises(AuthenticationException):
        User.authenticate(command)


def test_should_fail_when_username_is_not_long_enough():
    command = User.AuthenticationCommand(
        username="some",
        password="password",
        authentication=AUTHENTICATION_SUCCESS,
        token_generator=TOKEN_GENERATOR
    )

    with pytest.raises(AuthenticationException):
        User.authenticate(command)


def test_should_fail_when_password_is_not_long_enough():
    command = User.AuthenticationCommand(
        username="some",
        password="pass",
        authentication=AUTHENTICATION_SUCCESS,
        token_generator=TOKEN_GENERATOR
    )

    with pytest.raises(AuthenticationException):
        User.authenticate(command)
