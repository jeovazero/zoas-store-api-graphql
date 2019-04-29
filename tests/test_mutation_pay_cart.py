from .helpers import create_cart, get_session, put_product_cart, pay_cart
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
        "cardNumber": "534553523434534",
        "expiration_date": "01/27",
        "cvv": "123",
    },
}

# Fake user with wrong credicard number
john_wrong = copy.copy(john_right)
john_wrong["creditCard"] = {
    "cardNumber": "534553523434530",
    "expiration_date": "01/27",
    "cvv": "123",
}


def test_pay_cart(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10)
    put_product_cart(client, pid="1", qtd=20)

    resp2 = pay_cart(client, payload=john_right)
    json = resp2.get_json()
    data = json["data"]["payCart"]
    assert data["customer"] == "John Armless"
    assert data["totalPaid"] == 168.80
    assert len(data["productsPaid"]) == 2


def test_invalid_session(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10)
    put_product_cart(client, pid="1", qtd=20)

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "fake_session"

    resp2 = pay_cart(client, payload=john_right)
    json = resp2.get_json()

    assert json["data"]["payCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The session has expired or is invalid"
    )


def test_lack_of_stock(client):
    # First cart
    resp_1 = create_cart(client)
    assert len(get_session(resp_1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10)
    json_1 = put_product_cart(client, pid="1", qtd=20)

    assert json_1["data"]["payCart"] is not None

    # save the session
    session_1 = client.session_transaction()
    session_id_1 = session_1["u"]
    print("Session", session_1, session_id_1)

    # Second cart
    resp_2 = create_cart(client)
    assert len(get_session(resp_2)[1]) > 1
    # 11 (in cart 2) + 10 (in cart 1) > 20 (total of product 2)
    put_product_cart(client, pid="2", qtd=11)
    resp_pay_2 = pay_cart(client, payload=john_right)
    json_2 = resp_pay_2.get_json()
    data_2 = json_2["data"]["payCart"]
    assert data_2["customer"] == "John Armless"
    assert data_2["totalPaid"] == 141.68

    # Payment of cart 1
    with client.session_transaction() as session:
        session["u"] = session_id_1

    resp_pay_1 = pay_cart(client, payload=john_right)
    json_1 = resp_pay_1.get_json()

    assert json_1["data"]["payCart"] is None
    assert json_1["errors"] is not None
    assert (
        json_1["errors"][0]["message"]
        == 'The product "Zoas Agenda" has lack in the stock'
    )


def test_wrong_credit_card(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10)
    put_product_cart(client, pid="1", qtd=20)

    resp2 = pay_cart(client, payload=john_wrong)
    json = resp2.get_json()

    assert json["data"]["payCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "Problems in credit card informations"
    )
