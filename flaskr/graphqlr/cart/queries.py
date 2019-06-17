from graphene import List
from flask import session
from .types import ProductCart
from .helpers import resolve_list_product_cart
from flaskr.controllers import CartController


def resolve_cart(root, info):
    sid = str(session["u"])
    cart = CartController.get(id=sid)
    return resolve_list_product_cart(cart.products)


cart = List(ProductCart, resolver=resolve_cart)
