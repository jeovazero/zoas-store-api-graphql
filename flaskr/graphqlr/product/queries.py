from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from .types import Product

# from ..errors import INVALID_PRODUCT_ID


product = relay.Node.Field(Product)
products = SQLAlchemyConnectionField(Product)
