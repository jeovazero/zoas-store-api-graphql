from .helpers import api
from .helpers.func import new_uuid, add_fake_cart_products
from flaskr.controllers import CartController, ProductController
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

# Another fake user, invalid credit card with less than 16 digits
joao_fake = copy.deepcopy(john_right)
joao_fake["creditCard"] = {
    "cardNumber": "5345234345340",
    "expirationDate": "01/27",
    "cvv": "123",
}


def test_pay_cart(client):
    # add fake cart with products in database
    # pid=1, total_items=50, in_the_cart=20, unit_price=2, to_pay=$40
    # pid=2, total_items=20, in_the_cart=11, unit_price=12.88, to_pay=$141,68
    cart_id = add_fake_cart_products(client)

    # request
    mutation_id = new_uuid()
    response = api.pay_cart(client, payload=john_right, mutation_id=mutation_id)

    # json of response
    json = response.get_json()
    payload = json["data"]["payCart"]["payload"]
    client_mutation_id = json["data"]["payCart"]["clientMutationId"]

    product1_db = ProductController.get(id="1")
    product2_db = ProductController.get(id="2")

    # asserts
    # verify current quantity of products
    assert product1_db.avaliable == 30
    assert product2_db.avaliable == 9

    # verify if cart is empty
    products = CartController.get_products(id=cart_id)
    assert len(products) == 0

    # verify response
    assert client_mutation_id == mutation_id
    assert payload["customer"] == "John Armless"
    assert payload["totalPaid"] == 181.68
    assert len(payload["productsPaid"]) == 2


def test_invalid_session(client):
    # add fake cart with products in database
    add_fake_cart_products(client)

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "invalid_session"

    # request
    mutation_id = new_uuid()
    response = api.pay_cart(client, payload=john_right, mutation_id=mutation_id)

    # json of response
    json = response.get_json()

    # asserts
    assert json["data"]["payCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The session has expired or is invalid"
    )
    assert json["errors"][0]["code"] == "INVALID_SESSION"


def test_lack_of_stock(client):
    # First cart
    # - add fake cart with products in database
    # - pid=1, total_items=50, in_the_cart=20, unit_price=2, to_pay=$40
    # - pid=2, total_items=20, in_the_cart=11, unit_price=12.88, to_pay=$141,68
    add_fake_cart_products(client)

    # save the session
    with client.session_transaction() as session_1:
        session_id_1 = session_1["u"]

    # Second cart
    # same items
    add_fake_cart_products(client)

    # Payment of cart 2
    mutation_id_2 = new_uuid()
    response_2 = api.pay_cart(
        client, payload=john_right, mutation_id=mutation_id_2
    )
    json_2 = response_2.get_json()

    payload_2 = json_2["data"]["payCart"]["payload"]
    client_mutation_id = json_2["data"]["payCart"]["clientMutationId"]
    assert payload_2["customer"] == "John Armless"
    assert payload_2["totalPaid"] == 181.68
    assert client_mutation_id == mutation_id_2

    # Payment of cart 1
    with client.session_transaction() as session:
        session["u"] = session_id_1

    mutation_id_1 = new_uuid()
    response_1 = api.pay_cart(
        client, payload=john_right, mutation_id=mutation_id_1
    )
    json_1 = response_1.get_json()

    assert json_1["data"]["payCart"] is None
    assert json_1["errors"] is not None
    assert (
        json_1["errors"][0]["message"]
        == 'The product "Zoas Agenda" has lack in the stock'
    )
    assert json_1["errors"][0]["code"] == "LACK_OF_STOCK"


def test_wrong_credit_card(client):
    # add fake cart with products in database
    add_fake_cart_products(client)

    # request
    mutation_id = new_uuid()
    response = api.pay_cart(client, payload=john_wrong, mutation_id=mutation_id)

    # json of response
    json = response.get_json()

    # asserts
    assert json["data"]["payCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "Problems in credit card informations"
    )
    assert json["errors"][0]["code"] == "INVALID_CREDIT_CARD"


def test_wrong_credit_card_less_then_16(client):
    # add fake cart with products in database
    add_fake_cart_products(client)

    # request
    mutation_id = new_uuid()
    response = api.pay_cart(client, payload=joao_fake, mutation_id=mutation_id)

    # json of response
    json = response.get_json()

    # asserts
    assert json["data"]["payCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "Problems in credit card informations"
    )
    assert json["errors"][0]["code"] == "INVALID_CREDIT_CARD"
