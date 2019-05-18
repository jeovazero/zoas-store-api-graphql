from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from flaskr.database import ProductModel, PhotoModel

# from ..errors import INVALID_PRODUCT_ID


class Product(SQLAlchemyObjectType):
    """A product of store"""

    class Meta:
        model = ProductModel
        interfaces = (relay.Node,)


class Photo(SQLAlchemyObjectType):
    """A photo of a product"""

    class Meta:
        model = PhotoModel
        only_fields = ("url",)


class Products(relay.Connection):
    """A connection of products"""

    class Meta:
        node = Product
