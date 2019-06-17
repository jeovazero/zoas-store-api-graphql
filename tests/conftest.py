import pytest
from flaskr import create_app
from flaskr.database import CartController


@pytest.fixture(autouse=True, scope="function")
def setup_function(request):
    CartController.drop()


@pytest.fixture
def client():
    app = create_app("Testing")
    return app.test_client()
