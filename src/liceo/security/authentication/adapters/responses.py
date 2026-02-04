from typing import List
from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    @staticmethod
    def from_token(token: str):
        return TokenResponse(access_token=token, token_type="Bearer")
