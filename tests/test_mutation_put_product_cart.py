from .helpers import create_cart, get_session, put_product_cart, get_uuid


def test_put_product(client):
    mutation_id = get_uuid()
    resp1 = create_cart(client, mutation_id)
    assert len(get_session(resp1)[1]) > 1

    mutation_id = get_uuid()
    resp2 = put_product_cart(client, pid="2", qtd=10, uid=mutation_id)
    json = resp2.get_json()
    product_of_cart = json["data"]["putProductToCart"]["payload"][0]
    client_mutation_id = json["data"]["putProductToCart"]["clientMutationId"]

    assert product_of_cart["productId"] == 2
    assert product_of_cart["quantity"] == 10
    assert product_of_cart["price"] == 12.88
    assert len(product_of_cart["photos"]) == 2
    assert client_mutation_id == mutation_id


def test_invalid_session(client):
    mutation_id = get_uuid()
    resp1 = create_cart(client, mutation_id)
    assert len(get_session(resp1)[1]) > 1

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "fake_session"

    mutation_id = get_uuid()
    resp2 = put_product_cart(client, pid="2", qtd=10, uid=mutation_id)
    json = resp2.get_json()

    assert json["data"]["putProductToCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The session has expired or is invalid"
    )
    assert json["errors"][0]["code"] == "INVALID_SESSION"


def test_invalid_quantity_zero(client):
    mutation_id = get_uuid()
    resp1 = create_cart(client, mutation_id)
    assert len(get_session(resp1)[1]) > 1

    resp2 = put_product_cart(client, pid="2", qtd=0, uid=mutation_id)
    json = resp2.get_json()

    assert json["data"]["putProductToCart"] is None
    assert json["errors"] is not None
    assert json["errors"][0]["message"] == (
        "The product quantity must be greater than zero and less than total"
    )
    assert json["errors"][0]["code"] == "INVALID_PRODUCT_QUANTITY"


def test_invalid_quantity_greater(client):
    mutation_id = get_uuid()
    resp1 = create_cart(client, mutation_id)
    assert len(get_session(resp1)[1]) > 1

    resp2 = put_product_cart(client, pid="2", qtd=21, uid=mutation_id)
    json = resp2.get_json()

    assert json["data"]["putProductToCart"] is None
    assert json["errors"] is not None
    assert json["errors"][0]["message"] == (
        "The product quantity must be greater than zero and less than total"
    )
    assert json["errors"][0]["code"] == "INVALID_PRODUCT_QUANTITY"


def test_invalid_id(client):
    mutation_id = get_uuid()
    resp1 = create_cart(client, mutation_id)
    assert len(get_session(resp1)[1]) > 1

    resp2 = put_product_cart(client, pid="55", qtd=0, uid=mutation_id)
    json = resp2.get_json()

    assert json["data"]["putProductToCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The product with provided id not exist"
    )
    assert json["errors"][0]["code"] == "INVALID_PRODUCT_ID"
