from .helpers import api
from .helpers.func import add_fake_cart_products


def test_query_product_cart(client):
    # add fake cart with products in database
    add_fake_cart_products(client)

    # request
    response = api.get_product_cart(client, pid="2")

    # json of response
    json = response.get_json()
    product_cart = json["data"]["node"]

    # asserts
    assert product_cart["quantity"] == 11
    assert product_cart["productId"] == 2
    assert product_cart["title"] == "Zoas Agenda"


def test_invalid_session(client):
    # add fake cart with products in database
    add_fake_cart_products(client)

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "fake_session"

    # request
    response = api.get_product_cart(client, pid="2")

    # json of response
    json = response.get_json()

    assert json["data"]["node"] is None
