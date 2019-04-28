def test_query_products(client):
    resp = client.post(
        "/graphql",
        json={
            "query": """
            query {
                products {
                    hasMoreItems
                    items {
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
            """
        },
    )

    json = resp.get_json()

    products = json["data"]["products"]
    assert len(products["items"]) == 4
    assert products["hasMoreItems"] is False


def test_query_products_pagination(client):
    resp = client.post(
        "/graphql",
        json={
            "query": """
            query {
                products(offset: 1, limit: 2) {
                    hasMoreItems
                    items {
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
            """
        },
    )

    json = resp.get_json()

    products = json["data"]["products"]

    assert len(products["items"]) == 2
    assert products["hasMoreItems"] is True
