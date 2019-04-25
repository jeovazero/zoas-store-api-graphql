from graphene import Schema, ObjectType, List, Field, Int, Boolean
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..database import ProductModel, PhotoModel


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


class Query(ObjectType):
    products = Field(
        Products, offset=Int(default_value=0), limit=Int(default_value=10)
    )

    def resolve_products(self, info, **kwargs):
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 10)

        query = Item.get_query(info)
        total = query.count()

        items = query.offset(offset).limit(limit).all()
        has_more = (offset + limit) < total

        return Products(items=items, has_more_items=has_more)


schema = Schema(query=Query, types=[Products])
