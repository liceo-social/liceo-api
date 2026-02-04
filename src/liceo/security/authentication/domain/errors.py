from liceo.infra.domain.error import I18Error


class NotValidCredentials(I18Error):
    def __init__(self):
        super().__init__(
            "security.authentication.error.not_valid_credentials",
            "invalid credentials",
        )


class NotFoundUser(I18Error):
    def __init__(self):
        super().__init__(
            "security.authentication.error.not_found_user",
            "not user found with those credentials",
        )
