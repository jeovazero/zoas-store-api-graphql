from graphene import ObjectType, relay
from .cart.queries import cart as cart_query
from .product.queries import product as product_query
from .product.queries import products as products_query


class Query(ObjectType):
    cart = cart_query
    product = product_query
    products = products_query
    node = relay.Node.Field()
