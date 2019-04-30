from graphene import Schema
from .query import Query
from .mutation import Mutations
from .cart.types import Address
from .product.types import Products

schema = Schema(query=Query, mutation=Mutations, types=[Products, Address])
