import base64
from .types import ProductCart
from ..errors import (
    INVALID_PRODUCT_ID,
    INVALID_PRODUCT_QUANTITY,
    INVALID_CREDIT_CARD,
    ZoasError,
)


def decode_id(s):
    dec = base64.b64decode(s.encode("ascii")).decode("ascii")
    list_dec = dec.split(":")
    if len(list_dec) == 2:
        return list_dec[1]
    raise ZoasError(INVALID_PRODUCT_ID)


def b64encode(s):
    return base64.b64encode(s.encode("ascii")).decode("ascii")


def resolve_list_product_cart(products):
    ans = []
    for p in products:
        ans.append(ProductCart(p))
    return ans


def validate_product_quantity(product, quantity):
    avaliable = product.avaliable
    if quantity <= 0 or quantity > avaliable:
        raise ZoasError(INVALID_PRODUCT_QUANTITY)


def validate_credit_card(card):
    # Luhn algorithm
    if len(card) != 16:
        raise ZoasError(INVALID_CREDIT_CARD)
    s = 0
    for i in range(0, len(card)):
        v = ord(card[i]) - ord("0")
        if i & 1 == 1:
            s += v
        else:
            s += (v * 2) % 9
    if not (s % 10 == 0):
        raise ZoasError(INVALID_CREDIT_CARD)
