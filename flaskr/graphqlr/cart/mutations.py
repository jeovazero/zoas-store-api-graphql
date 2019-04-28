from graphene import List, String
from graphene import Mutation as MutationType
from flaskr.database import CartModel
from flaskr.database import Session as DbSession
from flask import session
import uuid
from .types import PutProductInput, ProductCart
from .helpers import (
    upsert_product_cart,
    resolve_list_product_cart,
    get_cart,
    get_product,
    get_product_cart,
)


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
        cart = get_cart(sid)
        DbSession.delete(cart)
        DbSession.commit()
        session.pop("u", None)
        return DeleteCart(confirmation="success")


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
        product = get_product(pid)

        sid = str(session["u"])
        product_cart = upsert_product_cart(sid, pid, product, quantity)

        # print("PUT PRODUCTS SESSION: ", session)
        cart = get_cart(sid)
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
        cart = get_cart(sid)

        # print("pid", pid, "sid", sid)
        product_cart = get_product_cart(sid, pid)
        DbSession.delete(product_cart)
        DbSession.commit()
        return resolve_list_product_cart(cart.products)
