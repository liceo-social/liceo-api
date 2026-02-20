from dataclasses import dataclass


@dataclass
class BasicDetailsError(Exception):
    field: str


class NoProjectsAttached(Exception):
    pass


class NoResponsible(Exception):
    pass


class ResponsibleNotFromProjects(Exception):
    pass
