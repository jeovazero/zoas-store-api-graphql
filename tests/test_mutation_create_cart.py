from .helpers import create_cart, get_session, get_uuid


def test_create_cart(client):
    mutation_id = get_uuid()
    resp = create_cart(client, mutation_id)
    json = resp.get_json()
    [session_name, session_value] = get_session(resp)

    assert len(session_value) > 1

    assert json["data"]["createCart"]["clientMutationId"] == mutation_id
    assert json["data"]["createCart"]["confirmation"] == "success"
