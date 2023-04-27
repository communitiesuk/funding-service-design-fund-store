from colored import attr
from colored import fg
from colored import stylize
from invoke import task

ECHO_STYLE = fg("light_gray") + attr("bold")


@task
def recreate_local_db(
    c, database_host="localhost", db_name="fsd_fund_store_1"
):
    """Create a clean database for testing"""
    c.run(f"dropdb -h {database_host} --if-exists {db_name} --force")
    print(
        stylize(
            f"{db_name} db dropped from {database_host}...",
            ECHO_STYLE,
        )
    )
    c.run(f"createdb -h {database_host} {db_name}")
    print(stylize(f"{db_name} db created on {database_host}...", ECHO_STYLE))


@task
def init_and_run_flask_migrate(
    c, database_host="localhost", db_name="fsd_fund_store_1"
):
    c.run("rm -rf ./db/migrations/")
    print(stylize("Deleted migrations", ECHO_STYLE))
    c.run("flask db init")
    print(
        stylize(
            "Run db init",
            ECHO_STYLE,
        )
    )
    c.run("flask db migrate -m 'Initial migration'")
    print(
        stylize(
            "Run migrate",
            ECHO_STYLE,
        )
    )
    c.run("flask db upgrade")
    print(
        stylize(
            "Run upgrade",
            ECHO_STYLE,
        )
    )
    c.run(f"psql -h {database_host} -d {db_name} -a -f db/cof_sql/fund.sql")
    c.run(f"psql -h {database_host} -d {db_name} -a -f db/cof_sql/rounds.sql")
    c.run(
        f'psql -h {database_host} -d {db_name} -c "select f.short_name as'
        " Fund, r.short_name as Round from round r join fund f on r.fund_id ="
        ' f.id";'
    )
