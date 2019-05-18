from ..models import CartModel, ProductCartModel
from .product import ProductController
from .. import Session
import os
from flaskr.graphqlr.errors import (
    INVALID_SESSION,
    INVALID_PRODUCT_ID,
    LACK_OF_STOCK,
    ZoasError,
)


IS_TESTING = os.getenv("FLASK_TESTING", False)


class CartController:
    @staticmethod
    def get_or_none(id: str):
        return Session.query(CartModel).filter_by(id=id).first()

    @staticmethod
    def get(id: str):
        cart = CartController.get_or_none(id)
        if not cart:
            raise ZoasError(INVALID_SESSION)
        return cart

    @staticmethod
    def create(id: str):
        cart = CartModel(id=id)
        Session.add(cart)
        Session.commit()

    @staticmethod
    def delete(id: str):
        cart = CartController.get(id=id)
        Session.delete(cart)
        Session.commit()

    @staticmethod
    def drop():
        try:
            for x in Session.query(CartModel).all():
                Session.delete(x)
            Session.commit()
        except Exception:
            print("Error in delete all data of Cart table")

    @staticmethod
    def put_product(id: str, pid: str, quantity: int):
        product_cart = CartController.get_product_or_none(id=id, pid=pid)

        if product_cart is None:
            product = ProductController.get(id=pid)
            product_cart = ProductCartModel(product=product, quantity=quantity)
        else:
            product_cart.quantity = quantity

        cart = CartController.get(id=id)
        cart.products.append(product_cart)

        Session.add(product_cart)
        Session.add(cart)
        Session.commit()

    @staticmethod
    def remove_product(id: str, pid: str):
        product_cart = CartController.get_product(id=id, pid=pid)
        Session.delete(product_cart)
        Session.commit()

    @staticmethod
    def get_products(id: str):
        products = Session.query(ProductCartModel).filter_by(cart_id=id).all()
        return products

    @staticmethod
    def get_product_or_none(id: str, pid: str):
        return (
            Session.query(ProductCartModel)
            .filter_by(cart_id=id, product_id=pid)
            .first()
        )

    @staticmethod
    def get_product(id: str, pid: str):
        product = CartController.get_product_or_none(id=id, pid=pid)

        if not product:
            raise ZoasError(INVALID_PRODUCT_ID)

        return product

    @staticmethod
    def pay_products(id: str):
        products_cart = CartController.get_products(id=id)

        # verify if all products has stock
        for prod_cart in products_cart:
            product = prod_cart.product

            if product.avaliable < prod_cart.quantity:
                errorMsg = [
                    LACK_OF_STOCK[0].format(product.title),
                    LACK_OF_STOCK[1],
                ]
                raise ZoasError(errorMsg)

        total = 0.0
        # doing the payment
        for prod_cart in products_cart:
            product = prod_cart.product

            total += prod_cart.quantity * product.price
            product.avaliable -= prod_cart.quantity
            product.avaliability = product.avaliable != 0

            Session.add(product)
            Session.delete(prod_cart)

        Session.commit()
        return total
