from graphene import ObjectType, List, Boolean
from graphene_sqlalchemy import SQLAlchemyObjectType
from flaskr.database import ProductModel, PhotoModel


class Item(SQLAlchemyObjectType):
    class Meta:
        model = ProductModel


class Photo(SQLAlchemyObjectType):
    class Meta:
        model = PhotoModel
        only_fields = ("url",)


class Products(ObjectType):
    items = List(Item)
    has_more_items = Boolean()
