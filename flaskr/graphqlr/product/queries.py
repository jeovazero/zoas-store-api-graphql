from graphene import Field, Int, String
from .types import Products, Item
from ..errors import INVALID_PRODUCT_ID


def resolve_products(root, info, **kwargs):
    offset = kwargs.get("offset", 0)
    limit = kwargs.get("limit", 10)

    query = Item.get_query(info)
    total = query.count()

    items = query.offset(offset).limit(limit).all()
    has_more = (offset + limit) < total

    return Products(items=items, has_more_items=has_more)


def resolve_product(root, info, **kwargs):
    pid = kwargs.get("product_id")
    print("pid", pid)
    product = Item.get_query(info).filter_by(id=pid).first()
    if not product:
        raise Exception(INVALID_PRODUCT_ID)
    return product


product = Field(
    Item, product_id=String(required=True), resolver=resolve_product
)

products = Field(
    Products,
    offset=Int(default_value=0),
    limit=Int(default_value=10),
    resolver=resolve_products,
)
