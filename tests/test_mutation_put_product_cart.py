from .helpers import api
from .helpers.func import add_fake_cart, new_uuid
from flaskr.database import CartController


def test_put_product(client):
    # add fake cart to database
    cart_id = add_fake_cart(client)

    # request
    mutation_id = new_uuid()
    response = api.put_product_cart(client, pid="2", qtd=10, uid=mutation_id)

    # json of response
    json = response.get_json()
    product_of_cart = json["data"]["putProductToCart"]["payload"][0]
    client_mutation_id = json["data"]["putProductToCart"]["clientMutationId"]

    # asserts
    products_db = CartController.get_products(id=cart_id)
    product_db = products_db[0]

    assert len(products_db) == 1
    assert products_db is not None
    assert product_db.product_id == 2

    assert product_of_cart["productId"] == 2
    assert product_of_cart["quantity"] == 10
    assert product_of_cart["price"] == 12.88
    assert len(product_of_cart["photos"]) == 2
    assert client_mutation_id == mutation_id


def test_put_idempotent(client):
    # add fake cart to database
    cart_id = add_fake_cart(client)

    # requests
    mutation_id = new_uuid()
    api.put_product_cart(client, pid="2", qtd=8, uid=mutation_id)
    api.put_product_cart(client, pid="2", qtd=9, uid=mutation_id)
    response = api.put_product_cart(client, pid="2", qtd=10, uid=mutation_id)

    # json of response
    json = response.get_json()

    payload = json["data"]["putProductToCart"]["payload"]
    product_of_cart = payload[0]
    client_mutation_id = json["data"]["putProductToCart"]["clientMutationId"]

    products_db = CartController.get_products(id=cart_id)
    product_db = products_db[0]

    # asserts

    # db
    assert len(products_db) == 1
    assert products_db is not None
    assert product_db.product_id == 2

    # response
    assert len(payload) == 1
    assert product_of_cart["productId"] == 2
    assert product_of_cart["quantity"] == 10
    assert product_of_cart["price"] == 12.88
    assert len(product_of_cart["photos"]) == 2
    assert client_mutation_id == mutation_id


def test_invalid_session(client):
    # add fake cart to database
    add_fake_cart(client)

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "invalid_session"

    # request
    mutation_id = new_uuid()
    response = api.put_product_cart(client, pid="2", qtd=10, uid=mutation_id)

    # json of request
    json = response.get_json()

    # asserts
    assert json["data"]["putProductToCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The session has expired or is invalid"
    )
    assert json["errors"][0]["code"] == "INVALID_SESSION"


def test_invalid_quantity_zero(client):
    # add fake cart to database
    add_fake_cart(client)

    # request
    mutation_id = new_uuid()
    response = api.put_product_cart(client, pid="2", qtd=0, uid=mutation_id)

    # json of response
    json = response.get_json()

    # assert
    assert json["data"]["putProductToCart"] is None
    assert json["errors"] is not None
    assert json["errors"][0]["message"] == (
        "The product quantity must be greater than zero and less than total"
    )
    assert json["errors"][0]["code"] == "INVALID_PRODUCT_QUANTITY"


def test_invalid_quantity_greater(client):
    # add fake cart to database
    add_fake_cart(client)

    # request
    mutation_id = new_uuid()
    response = api.put_product_cart(client, pid="2", qtd=21, uid=mutation_id)

    # json of response
    json = response.get_json()

    # asserts
    assert json["data"]["putProductToCart"] is None
    assert json["errors"] is not None
    assert json["errors"][0]["message"] == (
        "The product quantity must be greater than zero and less than total"
    )
    assert json["errors"][0]["code"] == "INVALID_PRODUCT_QUANTITY"


def test_invalid_id(client):
    # add fake cart to database
    add_fake_cart(client)

    # request
    mutation_id = new_uuid()
    response = api.put_product_cart(client, pid="55", qtd=0, uid=mutation_id)

    # json of response
    json = response.get_json()

    # asserts
    assert json["data"]["putProductToCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The product with provided id not exist"
    )
    assert json["errors"][0]["code"] == "INVALID_PRODUCT_ID"
