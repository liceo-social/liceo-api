from dataclasses import dataclass


@dataclass
class CreateProjectDTO:
    name: str
    description: str
    created_by: str
