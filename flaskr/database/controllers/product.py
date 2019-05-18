from ..models import ProductModel
from .. import Session


class ProductController:
    @staticmethod
    def get(id: str):
        return Session.query(ProductModel).filter_by(id=id).first()
