from .helpers import (
    _create_cart,
    put_product_cart,
    remove_product_cart,
    get_uuid,
)


def test_mutation_remove_product_cart(client):
    _create_cart(client)

    mutation_id = get_uuid()
    put_product_cart(client, pid="2", qtd=10, uid=mutation_id)
    put_product_cart(client, pid="1", qtd=20, uid=mutation_id)

    resp2 = remove_product_cart(client, pid="2", uid=mutation_id)
    json = resp2.get_json()
    cart = json["data"]["removeProductOfCart"]
    product = cart["payload"][0]
    client_mutation_id = cart["clientMutationId"]

    assert len(cart["payload"]) == 1
    assert product["productId"] == 1
    assert product["quantity"] == 20
    assert product["price"] == 2
    assert len(product["photos"]) == 1
    assert client_mutation_id == mutation_id


def test_invalid_session(client):
    _create_cart(client)

    mutation_id = get_uuid()
    put_product_cart(client, pid="2", qtd=10, uid=mutation_id)
    put_product_cart(client, pid="1", qtd=20, uid=mutation_id)

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "fake_session"

    resp2 = remove_product_cart(client, pid="2", uid=mutation_id)
    json = resp2.get_json()

    assert json["data"]["removeProductOfCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The session has expired or is invalid"
    )
    assert json["errors"][0]["code"] == "INVALID_SESSION"


def test_invalid_id(client):
    _create_cart(client)

    mutation_id = get_uuid()
    put_product_cart(client, pid="2", qtd=10, uid=mutation_id)
    put_product_cart(client, pid="1", qtd=20, uid=mutation_id)

    resp2 = remove_product_cart(client, pid="9", uid=mutation_id)
    json = resp2.get_json()

    assert json["data"]["removeProductOfCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The product with provided id not exist"
    )
    assert json["errors"][0]["code"] == "INVALID_PRODUCT_ID"
