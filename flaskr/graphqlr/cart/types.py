from graphene import ObjectType, List, Int, String, Float, InputObjectType


class PutProductInput(InputObjectType):
    productId = String()
    quantity = Int()


class PhotoProductCart(ObjectType):
    url = String()


class ProductCart(ObjectType):
    product_id = Int()
    title = String()
    description = String()
    price = Float()
    quantity = Int()
    photos = List(PhotoProductCart)
