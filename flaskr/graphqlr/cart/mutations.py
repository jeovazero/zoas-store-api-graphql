from graphene import List, String, Field, relay, ID, Int
from flaskr.controllers import CartController, ProductController
from ..mixins import SessionMixin
from .types import ProductCart, PurchaseResult, AddressInput, CreditCardInput
from .helpers import (
    resolve_list_product_cart,
    validate_product_quantity,
    validate_credit_card,
    decode_id,
)


class CreateCart(relay.ClientIDMutation, SessionMixin):
    confirmation = String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # create a session for the user
        cls.create_session()

        # create a register in the database
        CartController.create(id=cls.sid())

        return CreateCart(confirmation="success")


class DeleteCart(relay.ClientIDMutation, SessionMixin):
    confirmation = String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # remove the register from database
        CartController.delete(id=cls.sid())

        # delete the session
        cls.delete_session()

        return DeleteCart(confirmation="success")


class PutProductToCart(relay.ClientIDMutation, SessionMixin):
    class Input:
        id = ID(required=True)
        quantity = Int(required=True)

    payload = List(ProductCart)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # getting product id and quantity of product
        pid = decode_id(str(kwargs.get("id")))
        quantity = kwargs.get("quantity")

        # getting the cart if it exists
        cart = CartController.get(id=cls.sid())

        # get the product
        product = ProductController.get(id=pid)

        # validate if the quantity is valid
        validate_product_quantity(product, quantity)

        # putting the product
        CartController.put_product(id=cls.sid(), pid=pid, quantity=quantity)

        # return the updated cart
        return PutProductToCart(
            payload=resolve_list_product_cart(cart.products)
        )


class RemoveProductOfCart(relay.ClientIDMutation, SessionMixin):
    class Input:
        id = ID(required=True)

    payload = List(ProductCart)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # getting the product id
        pid = decode_id(kwargs.get("id"))

        # getting the cart if it exists
        cart = CartController.get(id=cls.sid())

        # remove the product
        CartController.remove_product(id=cls.sid(), pid=pid)

        # return the updated cart
        return RemoveProductOfCart(
            payload=resolve_list_product_cart(cart.products)
        )


class PayCart(relay.ClientIDMutation, SessionMixin):
    class Input:
        full_name = String(required=True)
        address = AddressInput(required=True)
        credit_card = CreditCardInput(required=True)

    payload = Field(PurchaseResult)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # read params
        fullname = kwargs.get("full_name")
        creditcard_in = kwargs.get("credit_card")
        address_in = kwargs.get("address")
        card_number = creditcard_in["card_number"]

        # getting the cart if it exists
        cart = CartController.get(id=cls.sid())

        # validate the credit card number
        validate_credit_card(card_number)

        # possible list of paid products
        products_paid = resolve_list_product_cart(cart.products)

        # processing the payment
        total_paid = CartController.pay_products(id=cls.sid())

        return PayCart(
            payload=PurchaseResult(
                customer=fullname,
                address=address_in,
                total_paid=total_paid,
                products_paid=products_paid,
            )
        )
