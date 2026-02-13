from pytest_archon import archrule


def test_service_contracts_should_extend_abstract_service():
    (

        archrule(
            name="service interfaces",
            comment="service contracts should extend AbstractService",
            use_regex=True
        )
        .exclude("liceo.mail")
        .match(r"liceo\..*\.application.service")
        .should_import("liceo.labs.db.core")
        .check("liceo")
    )


def test_service_implementations_should_implement_their_contrats():
    (
        archrule(
            name="service implementations",
            comment="service implementations should implement their contracts",
            use_regex=True
        )
        .match(r"liceo\..*\.adapters.service")
        .should_import("..application.service")
        .check("liceo")
    )


def test_service_contracts_should_not_import_repositories():
    (

        archrule(
            name="contracts-not-repositories",
            comment="contracts should not import repositories",
            use_regex=True
        )
        .match(r"liceo\..*\.application.service")
        .should_not_import("repository")
        .check("liceo")
    )
