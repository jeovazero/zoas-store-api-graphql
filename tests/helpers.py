import uuid
import base64


def get_uuid():
    return str(uuid.uuid4())


def encode_base64(s):
    return base64.b64encode(s.encode("ascii")).decode("ascii")


def create_cart(client, uid):
    return client.post(
        "/graphql",
        json={
            "query": """
            mutation {
                createCart(input: {"""
            f'clientMutationId: "{uid}"'
            """}) {
                    clientMutationId
                    confirmation
                }
            }
            """
        },
    )


def _create_cart(client):
    mutation_id = get_uuid()
    resp1 = create_cart(client, mutation_id)
    assert len(get_session(resp1)[1]) > 1


def delete_cart(client, mutation_id):
    return client.post(
        "/graphql",
        json={
            "query": """
            mutation{
                deleteCart(input: {"""
            f'clientMutationId: "{mutation_id}"'
            """}){
                    clientMutationId
                    confirmation
                }
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
                    id
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


def put_product_cart(client, pid, qtd, uid):
    id = encode_base64(f"Product:{pid}")
    return client.post(
        "/graphql",
        json={
            "query": """
            mutation {
                putProductToCart(input: {"""
            f'id: "{id}", quantity: {qtd}, clientMutationId: "{uid}"'
            """}){
                    clientMutationId
                    payload{
                        id
                        productId
                        quantity
                        price
                        photos {
                            url
                        }
                    }
                }
            }
            """
        },
    )


def _put_products(client):
    mutation_id = get_uuid()
    put_product_cart(client, pid="2", qtd=10, uid=mutation_id)
    put_product_cart(client, pid="1", qtd=20, uid=mutation_id)


def remove_product_cart(client, pid, uid):
    id = encode_base64(f"ProductCart:{pid}")
    return client.post(
        "/graphql",
        json={
            "query": """
            mutation {
            removeProductOfCart(input: {"""
            f'id: "{id}", clientMutationId: "{uid}"'
            """})
                {
                    clientMutationId
                    payload{
                        id
                        productId
                        quantity
                        price
                        photos {
                            url
                        }
                    }
                }
            }
            """
        },
    )


def get_product(client, pid):
    id = encode_base64(f"Product:{pid}")
    return client.post(
        "/graphql",
        json={
            "query": """
            query {"""
            f'product(id: "{id}")'
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


def get_product_cart(client, pid):
    id = encode_base64(f"ProductCart:{pid}")
    return client.post(
        "/graphql",
        json={
            "query": """
            query {"""
            f'node(id: "{id}")'
            """{
                ...on ProductCart {
                        id
                        title
                        productId
                        quantity
                        price
                        photos {
                            url
                        }
                    }
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


def pay_cart(client, payload, mutation_id):
    client_mutation_id = f'clientMutationId: "{mutation_id}"'
    params = unpack_dict(payload) + ", " + client_mutation_id
    mutation = (
        """
        mutation {
        payCart(input: {"""
        f"{params}"
        """})
        {
            clientMutationId
            payload{
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
                    id
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
        }
    """
    )

    return client.post("/graphql", json={"query": mutation})
