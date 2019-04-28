from .helpers import create_cart, get_session, put_product_cart


def test_put_product(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    resp2 = put_product_cart(client, pid="2", qtd=10)
    json = resp2.get_json()

    product_of_cart = json["data"]["putProductToCart"][0]
    assert product_of_cart["productId"] == 2
    assert product_of_cart["quantity"] == 10
    assert product_of_cart["price"] == 12.88
    assert len(product_of_cart["photos"]) == 2


def test_invalid_session(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "fake_session"

    resp2 = put_product_cart(client, pid="2", qtd=10)
    json = resp2.get_json()

    assert json["data"]["putProductToCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The session has expired or is invalid"
    )


def test_invalid_quantity_zero(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    resp2 = put_product_cart(client, pid="2", qtd=0)
    json = resp2.get_json()

    assert json["data"]["putProductToCart"] is None
    assert json["errors"] is not None
    assert json["errors"][0]["message"] == (
        "The product quantity must be greater than zero and less than total"
    )


def test_invalid_quantity_greater(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    resp2 = put_product_cart(client, pid="2", qtd=21)
    json = resp2.get_json()

    assert json["data"]["putProductToCart"] is None
    assert json["errors"] is not None
    assert json["errors"][0]["message"] == (
        "The product quantity must be greater than zero and less than total"
    )


def test_invalid_id(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    resp2 = put_product_cart(client, pid="5", qtd=0)
    json = resp2.get_json()

    assert json["data"]["putProductToCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The product with provided id not exist"
    )
