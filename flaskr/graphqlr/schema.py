from graphene import (
    Schema,
    ObjectType,
    List,
    Field,
    Int,
    Boolean,
    String,
    Float,
    InputObjectType,
)
from graphene import Mutation as MutationType
from graphene_sqlalchemy import SQLAlchemyObjectType
from ..database import ProductModel, PhotoModel, CartModel, ProductCartModel
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
        # print("CREATE PREVIOUS SESSION: ", session)
        session["u"] = uuid.uuid4()
        DbSession.add(CartModel(id=session["u"]))
        DbSession.commit()
        return CreateCart(confirmation="success")


class DeleteCart(MutationType):
    confirmation = String()

    def mutate(self, info):
        # print("DELETE PREVIOUS SESSION", session)
        sid = str(session["u"])
        cart = DbSession.query(CartModel).filter(CartModel.id == sid).first()
        DbSession.delete(cart)
        DbSession.commit()
        session.pop("u", None)
        return DeleteCart(confirmation="success")


class PutProductInput(InputObjectType):
    productId = String()
    quantity = Int()


class ProductCart(ObjectType):
    product_id = Int()
    title = String()
    description = String()
    price = Float()
    quantity = Int()
    photos = List(Photo)


def resolve_list_product_cart(products):
    ans = []
    for p in products:
        ans.append(resolve_product_cart(p))
    return ans


def resolve_product_cart(prodcart):
    return ProductCart(
        product_id=prodcart.product_id,
        title=prodcart.product.title,
        description=prodcart.product.description,
        price=prodcart.product.price,
        quantity=prodcart.quantity,
        photos=prodcart.product.photos,
    )


def upsert_product_cart(sid, pid, product, quantity):
    product_cart_query = (
        DbSession.query(ProductCartModel)
        .filter(
            ProductCartModel.cart_id == sid, ProductCartModel.product_id == pid
        )
        .all()
    )

    if len(product_cart_query) == 0:
        return ProductCartModel(product=product, quantity=quantity)
    product_cart = product_cart_query[0]
    product_cart.quantity = quantity
    return product_cart


class PutProductToCart(MutationType):
    class Arguments:
        payload = PutProductInput(required=True)

    Output = List(ProductCart)

    def mutate(self, info, **kwargs):
        # print("PUT PRODUCTS SESSION: ", session)

        payload = kwargs.get("payload", {})
        pid = str(payload.get("productId"))
        quantity = payload.get("quantity")

        # print("pid", pid)
        product = (
            DbSession.query(ProductModel).filter(ProductModel.id == pid).one()
        )

        sid = str(session["u"])
        product_cart = upsert_product_cart(sid, pid, product, quantity)

        # print("PUT PRODUCTS SESSION: ", session)
        cart = DbSession.query(CartModel).filter(CartModel.id == sid).one()
        # print("CArt", cart.products)
        cart.products.append(product_cart)
        DbSession.add(product_cart)
        DbSession.add(cart)
        DbSession.commit()
        cart = DbSession.query(CartModel).filter(CartModel.id == sid).one()
        return resolve_list_product_cart(cart.products)


class RemoveProductOfCart(MutationType):
    class Arguments:
        product_id = String()

    Output = List(ProductCart)

    def mutate(self, info, **kwargs):
        pid = kwargs.get("product_id")
        sid = str(session["u"])
        # print("pid", pid, "sid", sid)
        DbSession.query(ProductCartModel).filter(
            ProductCartModel.cart_id == sid, ProductCartModel.product_id == pid
        ).delete()
        DbSession.commit()
        cart = DbSession.query(CartModel).filter(CartModel.id == sid).one()
        return resolve_list_product_cart(cart.products)


class Query(ObjectType):
    products = Field(
        Products, offset=Int(default_value=0), limit=Int(default_value=10)
    )
    cart = List(ProductCart)

    def resolve_products(self, info, **kwargs):
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", 10)

        query = Item.get_query(info)
        total = query.count()

        items = query.offset(offset).limit(limit).all()
        has_more = (offset + limit) < total

        return Products(items=items, has_more_items=has_more)

    def resolve_cart(self, info):
        sid = str(session["u"])
        cart = DbSession.query(CartModel).filter(CartModel.id == sid).one()
        return resolve_list_product_cart(cart.products)


class Mutations(ObjectType):
    create_cart = CreateCart.Field()
    delete_cart = DeleteCart.Field()
    put_product_to_cart = PutProductToCart.Field()
    remove_product_of_cart = RemoveProductOfCart.Field()


schema = Schema(query=Query, mutation=Mutations, types=[Products, CreateCart])
