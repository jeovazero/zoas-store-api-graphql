from .helpers import create_cart, get_session, put_product_cart


def test_query_get_cart(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10)
    put_product_cart(client, pid="1", qtd=20)

    resp2 = client.post(
        "/graphql",
        json={
            "query": """
            query {
                cart {
                    productId
                    quantity
                    price
                    photos {
                        url
                    }
                }
            }
            """
        },
    )

    json = resp2.get_json()
    cart = json["data"]["cart"]

    assert len(cart) == 2
    assert cart[0]["productId"] is not None
    assert cart[1]["productId"] is not None
