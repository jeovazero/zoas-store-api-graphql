from .helpers.func import new_uuid, get_session, add_fake_cart
from .helpers import api
from flaskr.controllers import CartController


def test_delete_cart(client):
    # add fake cart to database
    session_id = add_fake_cart(client)

    # request
    mutation_id = new_uuid()
    response = api.delete_cart(client, mutation_id)

    # json
    json = response.get_json()
    [session_name, session_value] = get_session(response)

    # verify if cart not exists
    cart = CartController.get_or_none(id=session_id)
    assert cart is None

    # assert
    assert len(session_value) == 0
    assert json["data"]["deleteCart"]["confirmation"] == "success"
    assert json["data"]["deleteCart"]["clientMutationId"] == mutation_id


def test_invalid_session(client):
    # add fake cart to database
    add_fake_cart(client)

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "invalid_session"

    # resquest
    mutation_id = new_uuid()
    response = api.delete_cart(client, mutation_id)

    # json
    json = response.get_json()

    # asserts
    assert json["data"]["deleteCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The session has expired or is invalid"
    )
    assert json["errors"][0]["code"] == "INVALID_SESSION"
