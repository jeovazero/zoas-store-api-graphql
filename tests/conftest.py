import pytest
from flaskr.app import app
from flaskr.database import CartController


@pytest.fixture(autouse=True, scope="function")
def setup_function(request):
    CartController.drop()


@pytest.fixture
def client():
    return app.test_client()
