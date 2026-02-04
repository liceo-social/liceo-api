from liceo.infra.domain.error import I18Error


class AuthenticationException(I18Error):
    def __init__(self):
        super().__init__(
            "security.auth.error.not_authenticated",
            "Invalid authentication",
        )
