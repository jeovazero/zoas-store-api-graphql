from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base


class ProductCartModel(Base):
    __tablename__ = "products_cart"

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    cart_id = Column(String, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("ProductModel", uselist=False)
