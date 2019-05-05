from .helpers import get_product, encode_base64


def test_query_product(client):
    resp = get_product(client, pid="4")
    json = resp.get_json()

    product = json["data"]["product"]
    assert product["id"] == encode_base64("Product:4")
    assert product["title"] == "Zoas Mousepad Model 2"
    assert product["avaliable"] == 9
    assert product["price"] == 30.7
    assert len(product["photos"]) == 1


def test_invalid_id(client):
    resp = get_product(client, pid="99")

    json = resp.get_json()

    assert json["data"]["product"] is None
