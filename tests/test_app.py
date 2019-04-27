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


def put_product_cart(client, pid, qtd):
    return client.post(
        "/graphql",
        json={
            "query": """
            mutation {
                putProductToCart(payload: {"""
            f'productId: "{pid}", quantity: {qtd}'
            """}){
                    productId
                    quantity
                    price
                    photos {
                        url
                    }
                }
            }
            """
        },
    )


def test_mutation_put_product_cart(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    resp2 = put_product_cart(client, pid="2", qtd=10)
    json = resp2.get_json()

    product_of_cart = json["data"]["putProductToCart"][0]
    assert product_of_cart["productId"] == 2
    assert product_of_cart["quantity"] == 10
    assert product_of_cart["price"] == 12.88
    assert len(product_of_cart["photos"]) == 2


def test_query_get_cart(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10)
    put_product_cart(client, pid="1", qtd=20)

    resp2 = client.post(
        "/graphql",
        json={
            "query": """
            query {
                cart {
                    productId
                    quantity
                    price
                    photos {
                        url
                    }
                }
            }
            """
        },
    )

    json = resp2.get_json()
    cart = json["data"]["cart"]

    assert len(cart) == 2
    assert cart[0]["productId"] is not None
    assert cart[1]["productId"] is not None


def test_mutation_remove_product_cart(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10)
    put_product_cart(client, pid="1", qtd=20)

    resp2 = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
                removeProductOfCart(productId: "2") {
                    productId
                    quantity
                    price
                    photos {
                        url
                    }
                }
            }
            """
        },
    )

    json = resp2.get_json()
    cart = json["data"]["removeProductOfCart"]
    product = cart[0]

    assert len(cart) == 1
    assert product["productId"] == 1
    assert product["quantity"] == 20
    assert product["price"] == 2
    assert len(product["photos"]) == 1
