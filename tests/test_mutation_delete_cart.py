from .helpers import create_cart, get_session, get_uuid, delete_cart


def test_delete_cart(client):
    mutation_id = get_uuid()
    resp1 = create_cart(client, mutation_id)
    assert len(get_session(resp1)[1]) > 1

    mutation_id = get_uuid()
    resp2 = delete_cart(client, mutation_id)

    json = resp2.get_json()
    [session_name, session_value] = get_session(resp2)

    assert len(session_value) == 0
    assert json["data"]["deleteCart"]["confirmation"] == "success"
    assert json["data"]["deleteCart"]["clientMutationId"] == mutation_id


def test_invalid_session(client):
    mutation_id = get_uuid()
    resp1 = create_cart(client, mutation_id)
    assert len(get_session(resp1)[1]) > 1

    # Setting the invalid session id
    with client.session_transaction() as session:
        session["u"] = "fake_session"

    mutation_id = get_uuid()
    resp2 = delete_cart(client, mutation_id)

    json = resp2.get_json()

    assert json["data"]["deleteCart"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The session has expired or is invalid"
    )
    assert json["errors"][0]["code"] == "INVALID_SESSION"
