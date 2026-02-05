from pydantic import BaseModel


class OAuth2PasswordJSON(BaseModel):
    username: str
    password: str
    scope: str = ""
    grant_type: str = "password"
