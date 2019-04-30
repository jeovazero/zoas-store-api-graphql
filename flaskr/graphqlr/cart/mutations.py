from graphene import List, String, Float, Field
from graphene import Mutation as MutationType
from flaskr.database import CartModel
from flaskr.database import Session as DbSession
from flask import session
import uuid
from .types import PutProductInput, ProductCart, PayCartInput, Address
from .helpers import (
    upsert_product_cart,
    resolve_list_product_cart,
    get_cart,
    get_product,
    get_product_cart,
    validate_product_quantity,
    validate_credit_card,
    pay_products_cart,
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
        sid = str(session["u"])
        cart = get_cart(sid)
        payload = kwargs.get("payload", {})
        pid = str(payload.get("productId"))
        quantity = payload.get("quantity")

        product = get_product(pid)
        validate_product_quantity(product, quantity)

        product_cart = upsert_product_cart(sid, pid, product, quantity)

        cart.products.append(product_cart)
        DbSession.add(product_cart)
        DbSession.add(cart)
        DbSession.commit()
        cart = DbSession.query(CartModel).filter(CartModel.id == sid).one()
        return resolve_list_product_cart(cart.products)


class RemoveProductOfCart(MutationType):
    class Arguments:
        product_id = String(required=True)

    Output = List(ProductCart)

    def mutate(self, info, **kwargs):
        pid = kwargs.get("product_id")
        sid = str(session["u"])
        cart = get_cart(sid)

        product_cart = get_product_cart(sid, pid)
        DbSession.delete(product_cart)
        DbSession.commit()
        return resolve_list_product_cart(cart.products)


class PayCart(MutationType):
    class Arguments:
        payload = PayCartInput(required=True)

    customer = String()
    address = Field(Address)
    total_paid = Float()
    products_paid = List(ProductCart)

    def mutate(self, info, **kwargs):
        # read params
        payload = kwargs.get("payload")
        fullname = payload.get("full_name")
        creditcard_in = payload.get("credit_card")
        address_in = payload.get("address")
        card_number = creditcard_in["card_number"]

        # read cart if exists
        sid = str(session["u"])
        cart = get_cart(sid)

        validate_credit_card(card_number)

        products_paid = resolve_list_product_cart(cart.products)

        total_paid = pay_products_cart(sid)

        return PayCart(
            customer=fullname,
            address=address_in,
            total_paid=total_paid,
            products_paid=products_paid,
        )
