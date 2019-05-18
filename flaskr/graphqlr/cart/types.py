from graphene import (
    ObjectType,
    List,
    Int,
    String,
    Float,
    InputObjectType,
    relay,
    Field,
)
from ..mixins import SessionMixin
from flaskr.database import ProductCartModel
from flaskr.database import Session as DbSession


class PhotoProductCart(ObjectType):
    """A photo of a product in the cart"""

    url = String()


class ProductCart(ObjectType, SessionMixin):
    """A product in the cart"""

    product_id = Int()
    title = String()
    description = String()
    price = Float()
    quantity = Int()
    photos = List(PhotoProductCart)

    class Meta:
        interfaces = (relay.Node,)

    @classmethod
    def get_node(cls, info, id):
        prod_cart = (
            DbSession.query(ProductCartModel)
            .filter_by(cart_id=cls.sid(), product_id=id)
            .first()
        )
        if prod_cart is not None:
            return ProductCart(prod_cart)
        return prod_cart

    def __init__(self, prodcart):
        self.id = prodcart.product_id
        self.product_id = prodcart.product_id
        self.title = prodcart.product.title
        self.description = prodcart.product.description
        self.price = prodcart.product.price
        self.quantity = prodcart.quantity
        self.photos = prodcart.product.photos


class Address(ObjectType):
    """A address of a customer"""

    city = String()
    country = String()
    zipcode = String()
    street = String()
    number = String()
    district = String()


class AddressInput(InputObjectType):
    """A address input of a customer"""

    city = String(required=True)
    country = String(required=True)
    zipcode = String(required=True)
    street = String(required=True)
    number = String(required=True)
    district = String(required=True)


class CreditCardInput(InputObjectType):
    """A credit card input of a customer"""

    card_number = String(required=True)
    expiration_date = String(required=True)
    cvv = String(required=True)


class PurchaseResult(ObjectType):
    """A purchase result of a customer"""

    customer = String()
    address = Field(Address)
    total_paid = Float()
    products_paid = List(ProductCart)
