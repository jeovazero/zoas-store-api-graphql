from .helpers.func import encode_base64


def test_query_products(client):
    resp = client.post(
        "/graphql",
        json={
            "query": """
            query {
                products {
                    pageInfo{
                        hasNextPage
                    }
                    edges {
                        node {
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
                }
            }
            """
        },
    )

    json = resp.get_json()

    products = json["data"]["products"]
    edges = products["edges"]
    assert len(edges) == 8
    assert products["pageInfo"]["hasNextPage"] is False


def test_query_products_pagination(client):
    cursor = encode_base64("arrayconnection:1")
    resp = client.post(
        "/graphql",
        json={
            "query": """
            query {"""
            f'products(after: "{cursor}", first: 2)'
            """{
                    pageInfo{
                        hasNextPage
                    }
                    edges {
                        cursor
                        node{
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
                }
            }
            """
        },
    )

    json = resp.get_json()

    products = json["data"]["products"]
    edges = products["edges"]
    assert len(edges) == 2
    assert edges[0]["cursor"] == encode_base64("arrayconnection:2")
    assert edges[1]["cursor"] == encode_base64("arrayconnection:3")
    assert products["pageInfo"]["hasNextPage"] is True
