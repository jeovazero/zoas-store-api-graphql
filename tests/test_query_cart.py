from .helpers import _create_cart, get_cart, _put_products


def test_query_get_cart(client):
    _create_cart(client)
    _put_products(client)

    resp2 = get_cart(client)
    json = resp2.get_json()
    cart = json["data"]["cart"]

    assert len(cart) == 2
    assert cart[0]["productId"] is not None
    assert cart[1]["productId"] is not None


def test_invalid_session(client):
    _create_cart(client)
    _put_products(client)

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "fake_session"

    resp2 = get_cart(client)
    json = resp2.get_json()

    assert json["data"]["cart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The session has expired or is invalid"
    )
    assert json["errors"][0]["code"] == "INVALID_SESSION"
