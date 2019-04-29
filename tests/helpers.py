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


def get_cart(client):
    return client.post(
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


def get_cookie(response):
    return response.headers["Set-Cookie"]


def get_session(response):
    cookie = get_cookie(response)
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


def remove_product_cart(client, pid):
    return client.post(
        "/graphql",
        json={
            "query": """
            mutation {"""
            f'removeProductOfCart(productId: "{pid}")'
            """{
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


def get_product(client, pid):
    return client.post(
        "/graphql",
        json={
            "query": """
            query {"""
            f'product(productId: "{pid}")'
            """{
                    id
                    title
                    photos {
                        url
                    }
                    price
                    description
                    avaliable
                    avaliability
                }
            }
            """
        },
    )


def unpack_dict(d):
    s = []
    for key, val in d.items():
        r = (
            ("{ " + unpack_dict(val) + " }")
            if isinstance(d[key], dict)
            else f'"{val}"'
        )
        s.append(f"{key}: {r}")
    return ",".join(s)


def pay_cart(client, payload):
    params = " { " + unpack_dict(payload) + " }"
    mutation = (
        """
        mutation {"""
        f"payCart(payload: {params} )"
        """{
            customer
            address {
                city
                country
                zipcode
                street
                number
                district
            }
            totalPaid
            productsPaid {
                productId
                title
                description
                photos {
                    url
                }
                price
                quantity
            }
          }
        }
    """
    )

    return client.post("/graphql", json={"query": mutation})
