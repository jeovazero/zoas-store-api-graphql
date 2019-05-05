from .helpers import (
    create_cart,
    get_session,
    put_product_cart,
    pay_cart,
    get_uuid,
)
import copy

# Fake user
john_right = {
    "fullName": "John Armless",
    "address": {
        "city": "Armless City",
        "country": "Brazil",
        "zipcode": "60000100",
        "street": "Street Armless",
        "number": "10",
        "district": "Disctrict 10",
    },
    "creditCard": {
        "cardNumber": "5345535234345344",
        "expirationDate": "01/27",
        "cvv": "123",
    },
}

# Fake user with wrong credicard number
john_wrong = copy.deepcopy(john_right)
john_wrong["creditCard"] = {
    "cardNumber": "5345535234345340",
    "expirationDate": "01/27",
    "cvv": "123",
}


def test_pay_cart(client):
    mutation_id = get_uuid()
    resp1 = create_cart(client, mutation_id)
    assert len(get_session(resp1)[1]) > 1

    mutation_id = get_uuid()
    put_product_cart(client, pid="2", qtd=10, uid=mutation_id)
    put_product_cart(client, pid="1", qtd=20, uid=mutation_id)

    mutation_id = get_uuid()
    resp2 = pay_cart(client, payload=john_right, mutation_id=mutation_id)
    json = resp2.get_json()
    payload = json["data"]["payCart"]["payload"]
    client_mutation_id = json["data"]["payCart"]["clientMutationId"]

    assert client_mutation_id == mutation_id
    assert payload["customer"] == "John Armless"
    assert payload["totalPaid"] == 168.80
    assert len(payload["productsPaid"]) == 2


def test_invalid_session(client):
    mutation_id = get_uuid()
    resp1 = create_cart(client, mutation_id)
    assert len(get_session(resp1)[1]) > 1

    mutation_id = get_uuid()
    put_product_cart(client, pid="2", qtd=10, uid=mutation_id)
    put_product_cart(client, pid="1", qtd=20, uid=mutation_id)

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "fake_session"

    mutation_id = get_uuid()
    resp2 = pay_cart(client, payload=john_right, mutation_id=mutation_id)
    json = resp2.get_json()

    assert json["data"]["payCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The session has expired or is invalid"
    )
    assert json["errors"][0]["code"] == "INVALID_SESSION"


def test_lack_of_stock(client):
    # First cart
    mutation_id = get_uuid()
    resp_1 = create_cart(client, mutation_id)
    assert len(get_session(resp_1)[1]) > 1

    put_product_cart(client, pid="3", qtd=6, uid=mutation_id)
    resp_put_1 = put_product_cart(client, pid="4", qtd=5, uid=mutation_id)

    json_1 = resp_put_1.get_json()
    assert not (json_1["data"]["putProductToCart"] is None)

    # save the session
    session_id_1 = ""
    with client.session_transaction() as session_1:
        session_id_1 = session_1["u"]

    # Second cart
    mutation_id = get_uuid()
    resp_2 = create_cart(client, mutation_id)
    assert len(get_session(resp_2)[1]) > 1
    # 6 (in cart 2) + 6 (in cart 1) > 11 (total of product 3)
    put_product_cart(client, pid="3", qtd=6, uid=mutation_id)
    resp_pay_2 = pay_cart(client, payload=john_right, mutation_id=mutation_id)
    json_2 = resp_pay_2.get_json()
    payload_2 = json_2["data"]["payCart"]["payload"]
    client_mutation_id = json_2["data"]["payCart"]["clientMutationId"]
    assert payload_2["customer"] == "John Armless"
    assert payload_2["totalPaid"] == 184.5
    assert client_mutation_id == mutation_id

    # Payment of cart 1
    with client.session_transaction() as session:
        session["u"] = session_id_1

    mutation_id = get_uuid()
    resp_pay_1 = pay_cart(client, payload=john_right, mutation_id=mutation_id)
    json_1 = resp_pay_1.get_json()

    assert json_1["data"]["payCart"] is None
    assert json_1["errors"] is not None
    assert (
        json_1["errors"][0]["message"]
        == 'The product "Zoas Mousepad Model 1" has lack in the stock'
    )
    assert json_1["errors"][0]["code"] == "LACK_OF_STOCK"


def test_wrong_credit_card(client):
    mutation_id = get_uuid()
    resp1 = create_cart(client, mutation_id)
    assert len(get_session(resp1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10, uid=mutation_id)
    put_product_cart(client, pid="1", qtd=20, uid=mutation_id)

    mutation_id = get_uuid()
    resp2 = pay_cart(client, payload=john_wrong, mutation_id=mutation_id)
    json = resp2.get_json()

    assert json["data"]["payCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "Problems in credit card informations"
    )
    assert json["errors"][0]["code"] == "INVALID_CREDIT_CARD"
