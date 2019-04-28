from flaskr.database import Session as DbSession
from flaskr.database import ProductCartModel, CartModel, ProductModel
from .types import ProductCart
from ..errors import (
    INVALID_SESSION,
    INVALID_PRODUCT_ID,
    INVALID_PRODUCT_QUANTITY,
)


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


def get_cart(sid):
    cart = DbSession.query(CartModel).filter(CartModel.id == sid).first()

    if not cart:
        raise Exception(INVALID_SESSION)
    return cart


def get_product(pid):
    product = (
        DbSession.query(ProductModel).filter(ProductModel.id == pid).first()
    )

    if not product:
        raise Exception(INVALID_PRODUCT_ID)
    return product


def get_product_cart(sid, pid):
    product = (
        DbSession.query(ProductCartModel)
        .filter(
            ProductCartModel.cart_id == sid, ProductCartModel.product_id == pid
        )
        .first()
    )

    if not product:
        raise Exception(INVALID_PRODUCT_ID)
    return product


def validate_product_quantity(product, quantity):
    avaliable = product.avaliable
    if quantity <= 0 or quantity > avaliable:
        raise Exception(INVALID_PRODUCT_QUANTITY)
