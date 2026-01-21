from liceo.infra.domain.error import I18Error


class NotChangedBySameUserError(I18Error):
    def __init__(self):
        super().__init__(
            "security.users.error.not_changed_by_same_user",
            "property can only be changed by user",
        )


class RepeatedPasswordNotCorrect(I18Error):
    def __init__(self):
        super().__init__(
            "security.users.error.repeated_password",
            "repeated password is not correct",
        )


class RoleAddedByNoAdmin(I18Error):
    def __init__(self):
        super().__init__(
            "security.users.error.role_added_by_no_admin",
            "role added by a non admin user",
        )


class RoleRemovedByNoAdmin(I18Error):
    def __init__(self):
        super().__init__(
            "security.users.error.role_removed_by_no_admin",
            "role removed by a non admin user",
        )
