from ..models import CartModel
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
