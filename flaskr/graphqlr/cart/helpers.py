from flaskr.database import Session as DbSession
from flaskr.database import ProductCartModel, CartModel, ProductModel
from .types import ProductCart
from ..errors import (
    INVALID_SESSION,
    INVALID_PRODUCT_ID,
    INVALID_PRODUCT_QUANTITY,
    INVALID_CREDIT_CARD,
    LACK_OF_STOCK,
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


def validate_credit_card(card):
    # Luhn algorithm
    if len(card) != 16:
        raise Exception(INVALID_CREDIT_CARD)
    s = 0
    for i in range(0, len(card)):
        v = ord(card[i]) - ord("0")
        if i & 1 == 1:
            s += v
        else:
            s += (v * 2) % 9
    if not (s % 10 == 0):
        raise Exception(INVALID_CREDIT_CARD)


def pay_products_cart(sid):
    products_cart = (
        DbSession.query(ProductCartModel)
        .filter(ProductCartModel.cart_id == sid)
        .all()
    )
    total = 0.0
    for prod_cart in products_cart:
        product = prod_cart.product
        if product.avaliable >= prod_cart.quantity:
            total += prod_cart.quantity * product.price
            product.avaliable -= prod_cart.quantity
            product.avaliability = product.avaliable != 0
            DbSession.add(product)
            DbSession.delete(prod_cart)
        else:
            raise Exception(LACK_OF_STOCK.format(product.title))
    DbSession.commit()
    return total
