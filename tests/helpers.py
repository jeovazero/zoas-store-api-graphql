def create_cart(client):
    return client.post(
        "/graphql",
        json={
            "query": """
            mutation {
                createCart { confirmation }
            }
            """
        },
    )


def get_session(response):
    cookie = response.headers["Set-Cookie"]
    return cookie.split(";")[0].split("=")


def put_product_cart(client, pid, qtd):
    return client.post(
        "/graphql",
        json={
            "query": """
            mutation {
                putProductToCart(payload: {"""
            f'productId: "{pid}", quantity: {qtd}'
            """}){
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
