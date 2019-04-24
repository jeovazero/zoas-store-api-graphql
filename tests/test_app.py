import pytest
from src import app


@pytest.fixture
def client():
    return app.test_client()


def test_req(client):
    resp = client.post("/graphql", json={"query": "query { shirts { id } }"})

    json = resp.get_json()

    len_shirts = len(json["data"]["shirts"])

    assert len_shirts == 4
