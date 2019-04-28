from .helpers import create_cart, get_session


def test_create_cart(client):
    resp = create_cart(client)
    json = resp.get_json()
    [session_name, session_value] = get_session(resp)

    assert len(session_value) > 1
    assert json["data"]["createCart"]["confirmation"] == "success"
