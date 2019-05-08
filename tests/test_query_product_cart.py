from .helpers import _create_cart, get_product_cart, _put_products


def test_query_product_cart(client):
    _create_cart(client)
    _put_products(client)

    resp2 = get_product_cart(client, pid="2")
    json = resp2.get_json()
    product_cart = json["data"]["node"]

    assert product_cart["quantity"] == 10
    assert product_cart["productId"] == 2
    assert product_cart["title"] == "Zoas Agenda"


def test_invalid_session(client):
    _create_cart(client)
    _put_products(client)

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "fake_session"

    resp2 = get_product_cart(client, pid="2")
    json = resp2.get_json()

    assert json["data"]["node"] is None
