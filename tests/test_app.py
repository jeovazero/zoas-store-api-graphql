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


def test_mutation_create_cart(client):
    resp = create_cart(client)
    json = resp.get_json()
    cookie = resp.headers["Set-Cookie"]
    [session_name, session_value] = cookie.split(";")[0].split("=")

    assert len(session_value) > 1
    assert json["data"]["createCart"]["confirmation"] == "success"


"""
def test_mutation_delete_cart(client):
    with client.session_transaction() as session:
        session['u']='fake_cookie'

    resp = client.post(
        "/graphql",
        json={
            "query": ""
            mutation {
                deleteCart { confirmation }
            }
            ""
        },
    )

    print(resp.headers['Set-Cookie'].split(';'))
    assert len(resp.headers['Set-Cookie']) == 0
"""
