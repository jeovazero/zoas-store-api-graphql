from .helpers import api
from .helpers.func import get_session, new_uuid, get_cart_id
from flaskr.database import CartController


def test_create_cart(client):
    # request
    mutation_id = new_uuid()
    response = api.create_cart(client, mutation_id)
    json = response.get_json()
    [session_name, session_value] = get_session(response)

    cart_id = get_cart_id(session_value)
    cart = CartController.get(id=cart_id)

    # assert
    assert len(session_value) > 1
    assert json["data"]["createCart"]["clientMutationId"] == mutation_id
    assert json["data"]["createCart"]["confirmation"] == "success"
    assert cart is not None
