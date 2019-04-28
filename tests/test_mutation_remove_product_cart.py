from .helpers import create_cart, get_session, put_product_cart


def test_mutation_remove_product_cart(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    put_product_cart(client, pid="2", qtd=10)
    put_product_cart(client, pid="1", qtd=20)

    resp2 = client.post(
        "/graphql",
        json={
            "query": """
            mutation {
                removeProductOfCart(productId: "2") {
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
    cart = json["data"]["removeProductOfCart"]
    product = cart[0]

    assert len(cart) == 1
    assert product["productId"] == 1
    assert product["quantity"] == 20
    assert product["price"] == 2
    assert len(product["photos"]) == 1
