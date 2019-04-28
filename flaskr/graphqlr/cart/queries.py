from graphene import List
from flask import session
from .types import ProductCart
from .helpers import resolve_list_product_cart, get_cart


def resolve_cart(root, info):
    sid = str(session["u"])
    cart = get_cart(sid)
    return resolve_list_product_cart(cart.products)


cart = List(ProductCart, resolver=resolve_cart)
