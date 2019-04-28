from .helpers import (
    create_cart,
    get_session,
    put_product_cart,
    remove_product_cart,
)


def test_mutation_remove_product_cart(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10)
    put_product_cart(client, pid="1", qtd=20)

    resp2 = remove_product_cart(client, pid="2")
    json = resp2.get_json()
    cart = json["data"]["removeProductOfCart"]
    product = cart[0]

    assert len(cart) == 1
    assert product["productId"] == 1
    assert product["quantity"] == 20
    assert product["price"] == 2
    assert len(product["photos"]) == 1


def test_invalid_session(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10)
    put_product_cart(client, pid="1", qtd=20)

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "fake_session"

    resp2 = remove_product_cart(client, pid="2")
    json = resp2.get_json()

    assert json["data"]["removeProductOfCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The session has expired or is invalid"
    )


def test_invalid_id(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10)
    put_product_cart(client, pid="1", qtd=20)

    resp2 = remove_product_cart(client, pid="9")
    json = resp2.get_json()

    assert json["data"]["removeProductOfCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The product with provided id not exist"
    )
