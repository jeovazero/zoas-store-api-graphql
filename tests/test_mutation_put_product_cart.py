from .helpers import create_cart, get_session, put_product_cart


def test_mutation_put_product_cart(client):
    resp1 = create_cart(client)
    assert len(get_session(resp1)[1]) > 1

    resp2 = put_product_cart(client, pid="2", qtd=10)
    json = resp2.get_json()

    product_of_cart = json["data"]["putProductToCart"][0]
    assert product_of_cart["productId"] == 2
    assert product_of_cart["quantity"] == 10
    assert product_of_cart["price"] == 12.88
    assert len(product_of_cart["photos"]) == 2
