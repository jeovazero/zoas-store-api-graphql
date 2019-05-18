from ..models import CartModel, ProductCartModel, ProductModel
from .. import Session


class CartController:
    @staticmethod
    def get(id: str):
        return Session.query(CartModel).filter_by(id=id).first()

    @staticmethod
    def create(id: str):
        cart = CartModel(id=id)
        Session.add(cart)
        Session.commit()

    @staticmethod
    def delete(id: str):
        card = CartController.get(id)
        Session.delete(card)
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
    def add_product(id: str, pid: str, quantity: int):
        try:
            cart = CartController.get(id=id)
            product = Session.query(ProductModel).filter_by(id=pid).first()
            product_cart = ProductCartModel(product=product, quantity=quantity)
            cart.products.append(product_cart)
            Session.add(product_cart)
            Session.add(cart)
            Session.commit()
        except Exception:
            print(f"Error in put a product in cart of id: {id}")

    @staticmethod
    def get_products(id: str):
        products = Session.query(ProductCartModel).filter_by(cart_id=id).all()
        return products

    @staticmethod
    def get_product(id: str, pid: str):
        product = (
            Session.query(ProductCartModel)
            .filter_by(cart_id=id, product_id=pid)
            .first()
        )
        return product
