from pytest_archon import archrule


def test_can_only_import_from_adapters():
    (

        archrule(
            name="di import adapters",
            comment="dependency injection should only import adapters",
            use_regex=True
        )
        .match(r"liceo\..*\.adapters.di$")
        .should_import(".*.adapters")
        .check("liceo")
    )
