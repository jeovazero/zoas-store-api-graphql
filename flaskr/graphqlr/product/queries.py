from graphene import Field, Int
from .types import Products, Item


def resolve_products(root, info, **kwargs):
    offset = kwargs.get("offset", 0)
    limit = kwargs.get("limit", 10)

    query = Item.get_query(info)
    total = query.count()

    items = query.offset(offset).limit(limit).all()
    has_more = (offset + limit) < total

    return Products(items=items, has_more_items=has_more)


products = Field(
    Products,
    offset=Int(default_value=0),
    limit=Int(default_value=10),
    resolver=resolve_products,
)
