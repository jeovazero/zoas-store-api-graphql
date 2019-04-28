from .helpers import create_cart, get_session


def test_delete_cart(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    resp2 = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
                deleteCart { confirmation }
            }
            """
        },
    )

    json = resp2.get_json()
    [session_name, session_value] = get_session(resp2)
    assert len(session_value) == 0
    assert json["data"]["deleteCart"]["confirmation"] == "success"
