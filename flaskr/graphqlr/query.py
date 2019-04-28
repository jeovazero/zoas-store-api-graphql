from graphene import ObjectType
from .product.queries import products as products_query
from .cart.queries import cart as cart_query


class Query(ObjectType):
    products = products_query
    cart = cart_query
