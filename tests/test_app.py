import pytest
from flaskr.app import app


@pytest.fixture
def client():
    return app.test_client()


def test_query_products(client):
    resp = client.post(
        "/graphql",
        json={
            "query": """
            query {
                products {
                    hasMoreItems
                    items {
                        id
                        title
                        photos {
                            url
                        }
                        price
                        description
                        avaliable
                        avaliability
                    }
                }
            }
            """
        },
    )

    json = resp.get_json()

    products = json["data"]["products"]
    assert len(products["items"]) == 4
    assert products["hasMoreItems"] is False


def test_query_products_pagination(client):
    resp = client.post(
        "/graphql",
        json={
            "query": """
            query {
                products(offset: 1, limit: 2) {
                    hasMoreItems
                    items {
                        id
                        title
                        photos {
                            url
                        }
                        price
                        description
                        avaliable
                        avaliability
                    }
                }
            }
            """
        },
    )

    json = resp.get_json()

    products = json["data"]["products"]

    assert len(products["items"]) == 2
    assert products["hasMoreItems"] is True


def create_cart(client):
    return client.post(
        "/graphql",
        json={
            "query": """
            mutation {
                createCart { confirmation }
            }
            """
        },
    )


def get_session(response):
    cookie = response.headers["Set-Cookie"]
    return cookie.split(";")[0].split("=")


def test_mutation_create_cart(client):
    resp = create_cart(client)
    json = resp.get_json()
    [session_name, session_value] = get_session(resp)

    assert len(session_value) > 1
    assert json["data"]["createCart"]["confirmation"] == "success"


def test_mutation_delete_cart(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    resp2 = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
                deleteCart { confirmation }
            }
            """
        },
    )

    json = resp2.get_json()
    [session_name, session_value] = get_session(resp2)
    assert len(session_value) == 0
    assert json["data"]["deleteCart"]["confirmation"] == "success"
