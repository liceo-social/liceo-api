from liceo.infra.domain.error import I18Error


class AttemptedByNoAdmin(I18Error):
    def __init__(self):
        super().__init__(
            "security.users.error.created_by_no_admin",
            "user created by a non admin user",
        )
