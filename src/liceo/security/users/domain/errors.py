from liceo.infra.domain.error import I18Error


class RepeatedPasswordNotCorrect(I18Error):
    def __init__(self):
        super().__init__(
            "security.users.error.repeated_password",
            "repeated password is not correct",
        )


class OldPasswordNotCorrect(I18Error):
    def __init__(self):
        super().__init__(
            "security.users.error.wrong_credentials",
            "credentials are not correct",
        )


class NotChangedBySameUserError(I18Error):
    def __init__(self):
        super().__init__(
            "security.users.error.not_changed_by_same_user",
            "property can only be changed by user",
        )


class AttemptedByNoAdmin(I18Error):
    def __init__(self):
        super().__init__(
            "security.users.error.created_by_no_admin",
            "user created by a non admin user",
        )


class EditedByOtherUser(I18Error):
    def __init__(self):
        super().__init__(
            "security.users.error.concurrent_modification",
            "user edited at the same time by another user",
        )


class MissingResetPasswordValues(I18Error):
    def __init__(self):
        super().__init__(
            "security.users.error.reset",
            "missing password or repeated password",
        )
