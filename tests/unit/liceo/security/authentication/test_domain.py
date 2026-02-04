import pytest
from liceo.security.authentication.domain.entities import User
from liceo.security.authentication.domain.vo import Authentication, UserId
from liceo.security.authentication.domain.errors import NotValidCredentials

TOKEN = "token"


def AUTHENTICATION_SUCCESS(username, password): return Authentication(
    user_id=UserId(id="1"), token=TOKEN)


def AUTHENTICATION_FAILS(username, password): return None


def test_should_authenticate_successfully_with_proper_credentials():
    command = User.AuthenticationCommand(
        username="username", password="password", authentication=AUTHENTICATION_SUCCESS)

    authenticated_user = User.authenticate(command)
    assert authenticated_user.token == TOKEN
    assert len(authenticated_user._events) == 1


def test_should_fail_when_missing_credentials():
    command = User.AuthenticationCommand(
        username=None, password=None, authentication=AUTHENTICATION_SUCCESS)

    with pytest.raises(NotValidCredentials):
        User.authenticate(command)


def test_should_fail_when_credentials_are_empty():
    command = User.AuthenticationCommand(
        username="", password="", authentication=AUTHENTICATION_SUCCESS)

    with pytest.raises(NotValidCredentials):
        User.authenticate(command)


def test_should_fail_when_username_is_not_long_enough():
    command = User.AuthenticationCommand(
        username="some", password="password", authentication=AUTHENTICATION_SUCCESS)

    with pytest.raises(NotValidCredentials):
        User.authenticate(command)


def test_should_fail_when_password_is_not_long_enough():
    command = User.AuthenticationCommand(
        username="some", password="pass", authentication=AUTHENTICATION_SUCCESS)

    with pytest.raises(NotValidCredentials):
        User.authenticate(command)
