import pytest
from flaskr import create_app
from flaskr.seed import seed_command


@pytest.fixture
def client():
    app = create_app("Testing")
    client = app.test_client()

    # pushing the context
    ctx = app.app_context()
    ctx.push()

    # runner for cli command
    runner = app.test_cli_runner()

    # invoke the seed-db command
    runner.invoke(seed_command)

    yield client

    ctx.pop()
