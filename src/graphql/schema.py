from graphene import Schema, ObjectType, List
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..db import ShirtModel

print(ShirtModel)


class Shirt(SQLAlchemyObjectType):
    class Meta:
        model = ShirtModel


class Query(ObjectType):
    shirts = List(Shirt)

    def resolve_shirts(self, info):
        query = Shirt.get_query(info)
        return query.all()


schema = Schema(query=Query, types=[Shirt])
