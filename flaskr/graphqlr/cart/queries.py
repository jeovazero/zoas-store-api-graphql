from graphene import List
from flaskr.database import CartModel
from flaskr.database import Session as DbSession
from flask import session
from .types import ProductCart
from .helpers import resolve_list_product_cart


def resolve_cart(root, info):
    sid = str(session["u"])
    cart = DbSession.query(CartModel).filter(CartModel.id == sid).one()
    return resolve_list_product_cart(cart.products)


cart = List(ProductCart, resolver=resolve_cart)
