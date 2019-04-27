from graphene import Schema, ObjectType, List, Field, Int, Boolean, String
from graphene import Mutation as MutationType
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..database import ProductModel, PhotoModel, CartModel
from ..database import Session as DbSession
from flask import session
import uuid


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


class CreateCart(MutationType):
    confirmation = String()

    def mutate(self, info):
        print("CREATE PREVIOUS SESSION: ", session)
        session["u"] = uuid.uuid4()
        DbSession.add(CartModel(id=session["u"]))
        DbSession.commit()
        return CreateCart(confirmation="success")


class DeleteCart(MutationType):
    confirmation = String()

    def mutate(self, info):
        print("DELETE PREVIOUS SESSION", session)
        sid = str(session["u"])
        DbSession.query(CartModel).filter(CartModel.id == sid).delete()
        DbSession.commit()
        session.pop("u", None)
        return DeleteCart(confirmation="success")


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


class Mutations(ObjectType):
    create_cart = CreateCart.Field()
    delete_cart = DeleteCart.Field()


schema = Schema(query=Query, mutation=Mutations, types=[Products, CreateCart])
