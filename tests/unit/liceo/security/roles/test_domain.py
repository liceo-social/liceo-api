from liceo.security.roles.domain.entities import Role
from liceo.security.roles.domain import vo


def ALLOWED_PERMISSION_FN(permissions, user_id): return True


def create_role():
    return Role.create(
        Role.CreateRoleCommand(
            next_id=lambda: vo.RoleId(id="roleid"),
            name="ADMIN",
            created_by=vo.UserId(id="creatorid"),
            check_permissions=ALLOWED_PERMISSION_FN
        )
    )


def test_create_role():
    role = create_role()

    assert role.id is not None
    assert role.id.id == "roleid"
    assert role.created_by
    assert role.created_at
    assert role.last_modified_by
    assert role.last_modified_at
    assert role.name == "ADMIN"


def test_add_permissions():
    role = create_role().add_permissions(
        Role.AddPermissionsCommand(
            added_by=vo.UserId("modifierid"),
            permissions=set([vo.PermissionId("p1"), vo.PermissionId("p2")]),
            check_permissions=ALLOWED_PERMISSION_FN
        ),
    )

    assert role.last_modified_by is not None
    assert role.last_modified_by.id == "modifierid"
    assert len(role.permissions) == 2


def test_permissions_are_not_duplicated():
    role = create_role().add_permissions(
        Role.AddPermissionsCommand(
            added_by=vo.UserId("modifierid"),
            permissions=set([vo.PermissionId("p1"), vo.PermissionId("p2")]),
            check_permissions=ALLOWED_PERMISSION_FN
        )
    )

    role = role.add_permissions(
        Role.AddPermissionsCommand(
            added_by=vo.UserId("modifier2id"),
            permissions=set([vo.PermissionId("p1"), vo.PermissionId("p2")]),
            check_permissions=ALLOWED_PERMISSION_FN
        )
    )

    assert role.last_modified_by is not None
    assert role.last_modified_by.id == "modifier2id"
    assert len(role.permissions) == 2


def test_remove_permissions():
    role = create_role()\
        .add_permissions(
            Role.AddPermissionsCommand(
                added_by=vo.UserId("modifierid"),
                permissions=set([vo.PermissionId("p1"), vo.PermissionId("p2")]),
                check_permissions=ALLOWED_PERMISSION_FN
            )
    )\
        .remove_permissions(
            Role.RemovePermissionsCommand(
                removed_by=vo.UserId("modifier2id"),
                permissions=set([vo.PermissionId("p2")]),
                check_permissions=ALLOWED_PERMISSION_FN
            )
    )

    assert role.last_modified_by.id == "modifier2id"
    assert len(role.permissions) == 1


def test_delete_role():
    role = create_role()\
        .add_permissions(
            Role.AddPermissionsCommand(
                added_by=vo.UserId("modifierid"),
                permissions=set([vo.PermissionId("p1"), vo.PermissionId("p2")]),
                check_permissions=ALLOWED_PERMISSION_FN
            )
    )\
        .remove_permissions(
            Role.RemovePermissionsCommand(
                removed_by=vo.UserId("modifier2id"),
                permissions=set([vo.PermissionId("p2")]),
                check_permissions=ALLOWED_PERMISSION_FN
            )
    ).delete(cmd=Role.DeleteRoleCommand(
        deleted_by=vo.UserId(id="deletedbyid"),
        check_permissions=ALLOWED_PERMISSION_FN
    ))

    assert len(role.permissions) == 0
    assert role.deleted_by is not None
    assert role.deleted_by.id == "deletedbyid"
    assert role.deleted_at is not None
