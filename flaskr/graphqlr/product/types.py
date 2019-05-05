from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from flaskr.database import ProductModel, PhotoModel

# from ..errors import INVALID_PRODUCT_ID


class Product(SQLAlchemyObjectType):
    class Meta:
        model = ProductModel
        interfaces = (relay.Node,)


class Photo(SQLAlchemyObjectType):
    class Meta:
        model = PhotoModel
        only_fields = ("url",)


class Products(relay.Connection):
    class Meta:
        node = Product
