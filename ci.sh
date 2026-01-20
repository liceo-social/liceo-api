function run_unit_tests {
    uv run coverage run -m pytest --disable-warnings --rootdir=tests/unit tests/unit
}

function run_arch_tests {
    uv run coverage run -m pytest --disable-warnings --rootdir=tests/architecture tests/architecture
}

function run_integration_tests {
    uv run coverage run -m pytest --disable-warnings --rootdir=tests/integration tests/integration
}

function run_coverage_report {
    uv run coverage html -d /tmp
}

function run_import_check {
    uv run isort -q --check src/ && uv run isort -q --check tests/
}

function run_lint {
    # uv run flake8 src/ && uv run flake8 tests/
    echo "LINT TBD"
}

function run_format_check {
    uv run ruff check -q src/ && uv run ruff check -q tests/
}

function run_format_sql_check {
    uv run sqlfluff lint src && uv run sqlfluff lint tests/
}

function run_check {
    run_format_check && run_format_sql_check && run_import_check && run_lint
}

function run_local_up {
    docker compose \
        --env-file ./docker/docker-compose/docker-compose-config.txt \
        up --build -d
}

function run_local_status {
    docker compose \
        --env-file ./docker/docker-compose/docker-compose-config.txt \
        ps
}

function run_local_down {
    docker compose \
        --env-file ./docker/docker-compose/docker-compose-config.txt \
        down && \
    docker volume rm $(docker volume list | grep "optiak_local" | awk '{ print $2 }')
}

function run_local {
    docker compose --env-file ./docker/docker-compose/docker-compose-config.txt $1
}

function run_local_logs {
    docker compose --env-file ./docker/docker-compose/docker-compose-config.txt logs -f $1
}

function run_gh_prepare {
    pipx ensurepath && pipx install poetry
}

function run_gh_poetry_env {
    source $(poetry env info --path)/bin/activate
}

function usage {
    echo "./ci.sh ["
    echo "   unit-tests |                --> runs unit tests"
    echo "   integration-tests |         --> runs integration tests"
    echo "   arch-tests |                --> runs architecture tests"
    echo "   coverage-report |           --> runs coverage report creation"
    echo "   check |                     --> runs linter, formater & imports checks"
    echo "   run-local                   --> executes docker-compose commands"
    echo "   run-local-up |              --> runs docker-compose up to bootstrap local environment"
    echo "   run-local-status |          --> runs docker-compose ps"
    echo "   run-local-down |            --> runs docker-compose down"
    echo "   run-local-logs {service} |  --> runs docker logs for {service-name}"
    echo "   lint |                      --> runs linter"
    echo "   format-check |              --> runs format check"
    echo "   import-check |              --> runs imports check"
    echo "   gh-prepare |                --> prepares Github Actions dependencies"
    echo "   gh-poetry-env |             --> activates poetry env"
    echo "]"
}

case $1 in
    gh-prepare)
        run_gh_prepare
        ;;
    gh-poetry-env)
        run_gh_poetry_env
        ;;
    run-local)
        run_local $2
        ;;
    run-local-up)
        run_local_up
        ;;
    run-local-status)
        run_local_status
        ;;
    run-local-down)
        run_local_down
        ;;
    run-local-logs)
        run_local_logs $2
        ;;
    check)
        run_check
        ;;
    format-check)
        run_format_check
        ;;
    lint)
        run_lint
        ;;
    import-check)
        run_import_check
        ;;
    unit-tests)
        run_unit_tests
        ;;
    integration-tests)
        run_integration_tests
        ;;
    arch-tests)
        run_arch_tests
        ;;
    coverage-report)
        run_coverage_report
        ;;
    *)
        usage
    ;;

esac