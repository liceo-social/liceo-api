from dataclasses import dataclass


@dataclass
class CredentialsDTO:
    username: str
    password: str
