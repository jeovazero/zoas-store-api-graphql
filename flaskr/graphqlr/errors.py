INVALID_SESSION = ["The session has expired or is invalid", "INVALID_SESSION"]
INVALID_PRODUCT_QUANTITY = [
    "The product quantity must be greater than zero and less than total",
    "INVALID_PRODUCT_QUANTITY",
]
INVALID_PRODUCT_ID = [
    "The product with provided id not exist",
    "INVALID_PRODUCT_ID",
]
INVALID_CREDIT_CARD = [
    "Problems in credit card informations",
    "INVALID_CREDIT_CARD",
]
LACK_OF_STOCK = ['The product "{}" has lack in the stock', "LACK_OF_STOCK"]


class ZoasError(Exception):
    def __init__(self, args):
        message, code = args
        self.message = message
        self.code = code
