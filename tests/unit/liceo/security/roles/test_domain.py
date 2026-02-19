from liceo.security.roles.domain.entities import Role
from liceo.security.roles.domain import vo


def ALLOWED_PERMISSION_FN(permissions, user_id): return True


def create_role():
    return Role.create(
        Role.CreateRoleCommand(
            next_id=lambda: vo.RoleId(id="roleid"),
            name="ADMIN",
            description="admin",
            created_by=vo.UserId(id="creatorid"),
            is_admin=True,
            permissions=set([vo.PermissionId(id="p1")])
        )
    )


def test_create_role():
    role = create_role()

    assert role.id is not None
    assert role.id.id == "roleid"
    assert role.created_by
    assert role.created_at
    assert role.last_updated_by
    assert role.last_updated_at
    assert role.name == "ADMIN"


def test_add_permissions():
    role = create_role().modify_permissions(
        Role.ModifyPermissionsCommand(
            expected_version=1,
            changed_by=vo.UserId("modifierid"),
            is_admin=True,
            permissions=set([vo.PermissionId(id="p1"), vo.PermissionId(id="p2")])
        ),
    )

    assert role.last_updated_by is not None
    assert role.last_updated_by.id == "modifierid"
    assert len(role.permissions) == 2


def test_permissions_are_not_duplicated():
    role = create_role().modify_permissions(
        Role.ModifyPermissionsCommand(
            expected_version=1,
            changed_by=vo.UserId("modifierid"),
            permissions=set([vo.PermissionId("p1"), vo.PermissionId("p2")]),
            is_admin=True
        )
    )

    role = role.modify_permissions(
        Role.ModifyPermissionsCommand(
            expected_version=2,
            changed_by=vo.UserId("modifier2id"),
            permissions=set([vo.PermissionId("p1"), vo.PermissionId("p2")]),
            is_admin=True
        )
    )

    assert role.last_updated_by is not None
    assert role.last_updated_by.id == "modifier2id"
    assert len(role.permissions) == 2


def test_delete_role():
    role = create_role()\
        .modify_permissions(
            Role.ModifyPermissionsCommand(
                expected_version=1,
                changed_by=vo.UserId("modifierid"),
                permissions=set([vo.PermissionId("p1"), vo.PermissionId("p2")]),
                is_admin=True
            )
    )\
        .delete(cmd=Role.DeleteRoleCommand(
            expected_version=2,
            deleted_by=vo.UserId(id="deletedbyid"),
            is_admin=True
        ))

    assert len(role.permissions) == 0
    assert role.deleted_by is not None
    assert role.deleted_by.id == "deletedbyid"
    assert role.deleted_at is not None
