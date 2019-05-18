from .helpers import api
from .helpers.func import add_fake_cart_products


def test_query_get_cart(client):
    # add fake cart with products in database
    add_fake_cart_products(client)

    # request
    response = api.get_cart(client)

    # json of response
    json = response.get_json()
    cart = json["data"]["cart"]

    # asserts
    assert len(cart) == 2
    assert cart[0]["productId"] == 1
    assert cart[1]["productId"] == 2


def test_invalid_session(client):
    # add fake cart with products in database
    add_fake_cart_products(client)

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "fake_session"

    # request
    response = api.get_cart(client)

    # json of response
    json = response.get_json()

    # asserts
    assert json["data"]["cart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The session has expired or is invalid"
    )
    assert json["errors"][0]["code"] == "INVALID_SESSION"
