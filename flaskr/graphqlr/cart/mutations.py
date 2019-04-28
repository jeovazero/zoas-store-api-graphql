from graphene import List, String
from graphene import Mutation as MutationType
from flaskr.database import ProductModel, CartModel, ProductCartModel
from flaskr.database import Session as DbSession
from flask import session
import uuid
from .types import PutProductInput, ProductCart
from .helpers import upsert_product_cart, resolve_list_product_cart


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
