from pytest_archon import archrule


# --8<-- [start:test_domain_should_not_import_adapters]
def test_domain_should_not_import_adapters():
    (
        archrule("domain", comment="domain should not import adapters")
        .match("liceo.security.users.domain.entities")
        .should_not_import("liceo.*.adapters*")
        .check("liceo.security.users.domain")
    )


# --8<-- [end:test_domain_should_not_import_adapters]


def test_domain_should_not_import_application():
    (
        archrule("domain", comment="domain should not import application")
        .match("liceo.security.users.domain.entities")
        .should_not_import("liceo.*.application*")
        .check("liceo.security.users.domain")
    )


def test_entities_can_use_value_objects():
    (
        archrule("domain", comment="domain can have value objects as dependencies")
        .match("liceo.security.users.domain*")
        .may_import("liceo.security.users.domain.vo")
        .check("liceo")
    )
