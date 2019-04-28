from flaskr.database import Session as DbSession
from flaskr.database import ProductCartModel
from .types import ProductCart


def resolve_list_product_cart(products):
    ans = []
    for p in products:
        ans.append(resolve_product_cart(p))
    return ans


def resolve_product_cart(prodcart):
    return ProductCart(
        product_id=prodcart.product_id,
        title=prodcart.product.title,
        description=prodcart.product.description,
        price=prodcart.product.price,
        quantity=prodcart.quantity,
        photos=prodcart.product.photos,
    )


def upsert_product_cart(sid, pid, product, quantity):
    product_cart_query = (
        DbSession.query(ProductCartModel)
        .filter(
            ProductCartModel.cart_id == sid, ProductCartModel.product_id == pid
        )
        .all()
    )

    if len(product_cart_query) == 0:
        return ProductCartModel(product=product, quantity=quantity)
    product_cart = product_cart_query[0]
    product_cart.quantity = quantity
    return product_cart
