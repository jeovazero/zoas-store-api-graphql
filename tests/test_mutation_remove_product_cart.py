from .helpers import api
from .helpers.func import new_uuid, add_fake_cart_products
from flaskr.database import CartController


def test_mutation_remove_product_cart(client):
    # add fake cart with products in database
    cart_id = add_fake_cart_products(client)

    # request
    mutation_id = new_uuid()
    response = api.remove_product_cart(client, pid="2", uid=mutation_id)

    # json of response
    json = response.get_json()

    cart = json["data"]["removeProductOfCart"]
    product = cart["payload"][0]
    client_mutation_id = cart["clientMutationId"]

    products_db = CartController.get_products(id=cart_id)

    # asserts
    assert len(products_db) == 1
    assert products_db[0].product_id == 1

    assert len(cart["payload"]) == 1
    assert product["productId"] == 1
    assert product["quantity"] == 20
    assert product["price"] == 2
    assert len(product["photos"]) == 1
    assert client_mutation_id == mutation_id


def test_invalid_session(client):
    # add fake cart with products in database
    add_fake_cart_products(client)

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "invalid_session"

    # request
    mutation_id = new_uuid()
    response = api.remove_product_cart(client, pid="2", uid=mutation_id)

    # json of response
    json = response.get_json()

    assert json["data"]["removeProductOfCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The session has expired or is invalid"
    )
    assert json["errors"][0]["code"] == "INVALID_SESSION"


def test_invalid_id(client):
    # add fake cart with products in database
    add_fake_cart_products(client)

    # request
    mutation_id = new_uuid()
    response = api.remove_product_cart(client, pid="9", uid=mutation_id)

    # json of response
    json = response.get_json()

    assert json["data"]["removeProductOfCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The product with provided id not exist"
    )
    assert json["errors"][0]["code"] == "INVALID_PRODUCT_ID"
