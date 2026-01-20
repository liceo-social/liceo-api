from liceo.security.permissions.domain.entities import Permission
from liceo.security.permissions.domain import vo


def new_permission():
    command = Permission.CreatePermissionCommand(
        name="USER_CREATE",
        created_by=vo.UserId(id="someuserid"),
        next_id=lambda: vo.PermissionId(id="id")
    )
    return Permission.create(command=command)


def test_create_permission():
    permission = new_permission()

    assert permission.id is not None
    assert permission.created_by.id == "someuserid"
    assert permission.created_at is not None
    assert permission.last_modified_by.id == "someuserid"
    assert permission.last_modified_at is not None
    assert permission.name == "USER_CREATE"


def test_change_name():
    permission = new_permission().change_name(
        command=Permission.ChangeNameCommand(
            new_name="USER_CREATE_ADDRESS",
            changed_by=vo.UserId(id="changerid")
        )
    )

    assert permission.id is not None
    assert permission.created_by.id == "someuserid"
    assert permission.last_modified_by.id == "changerid"
    assert permission.last_modified_at > permission.created_at
    assert permission.name == "USER_CREATE_ADDRESS"


def test_delete_permission():
    permission = new_permission().delete(
        command=Permission.DeletePermissionCommand(
            deleted_by=vo.UserId("deletedbyid")
        )
    )

    assert permission.id is not None
    assert permission.created_by.id == "someuserid"
    assert permission.last_modified_by.id == "someuserid"
    assert permission.deleted_by is not None
    assert permission.deleted_by.id == "deletedbyid"
    assert permission.deleted_at is not None
    assert permission.deleted_at > permission.created_at
