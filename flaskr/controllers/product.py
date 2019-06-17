from ..models import ProductModel
from flaskr import db
from flaskr.graphqlr.errors import INVALID_PRODUCT_ID, ZoasError


Session = db.session


class ProductController:
    @staticmethod
    def get(id: str):
        product = Session.query(ProductModel).filter_by(id=id).first()

        if not product:
            raise ZoasError(INVALID_PRODUCT_ID)
        else:
            return product
