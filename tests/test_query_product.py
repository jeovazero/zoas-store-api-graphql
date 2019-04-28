from .helpers import get_product


def test_query_product(client):
    resp = get_product(client, pid="4")
    json = resp.get_json()

    product = json["data"]["product"]
    assert product["id"] == "4"
    assert product["title"] == "Zoas Mousepad Model 2"
    assert product["avaliable"] == 9
    assert product["price"] == 30.7
    assert len(product["photos"]) == 1


def test_invalid_id(client):
    resp = get_product(client, pid="6")

    json = resp.get_json()

    assert json["data"]["product"] is None
    assert json["errors"] is not None
    assert (
        json["errors"][0]["message"] == "The product with provided id not exist"
    )
