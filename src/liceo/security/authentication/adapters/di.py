from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

AuthRequestDependency = Annotated[OAuth2PasswordRequestForm, Depends()]

AuthenticationServiceDependency = Annotated[object, Depends()]
