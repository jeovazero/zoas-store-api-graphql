from graphene import ObjectType
from .cart.mutations import (
    CreateCart,
    DeleteCart,
    PutProductToCart,
    RemoveProductOfCart,
)


class Mutations(ObjectType):
    create_cart = CreateCart.Field()
    delete_cart = DeleteCart.Field()
    put_product_to_cart = PutProductToCart.Field()
    remove_product_of_cart = RemoveProductOfCart.Field()
