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


class Address(ObjectType):
    city = String()
    country = String()
    zipcode = String()
    street = String()
    number = String()
    district = String()


class AddressInput(InputObjectType):
    city = String(required=True)
    country = String(required=True)
    zipcode = String(required=True)
    street = String(required=True)
    number = String(required=True)
    district = String(required=True)


class CreditCardInput(InputObjectType):
    card_number = String(required=True)
    expiration_date = String(required=True)
    cvv = String(required=True)


class PayCartInput(InputObjectType):
    full_name = String(required=True)
    address = AddressInput(required=True)
    credit_card = CreditCardInput(required=True)
