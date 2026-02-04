from fastapi import HTTPException, status


class AuthenticationException(HTTPException):
    def __init__(self):
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = "Incorrect username or password"
        self.headers = {"WWW-Authenticate": "Bearer"}
