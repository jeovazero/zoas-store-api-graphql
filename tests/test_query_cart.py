from .helpers import (
    create_cart,
    get_session,
    put_product_cart,
    get_cart,
    get_uuid,
)


def test_query_get_cart(client):
    mutation_id = get_uuid()
    resp1 = create_cart(client, mutation_id)
    assert len(get_session(resp1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10, uid=mutation_id)
    put_product_cart(client, pid="1", qtd=20, uid=mutation_id)

    resp2 = get_cart(client)
    json = resp2.get_json()
    cart = json["data"]["cart"]

    assert len(cart) == 2
    assert cart[0]["productId"] is not None
    assert cart[1]["productId"] is not None


def test_invalid_session(client):
    mutation_id = get_uuid()
    resp1 = create_cart(client, mutation_id)
    assert len(get_session(resp1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10, uid=mutation_id)
    put_product_cart(client, pid="1", qtd=20, uid=mutation_id)

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
