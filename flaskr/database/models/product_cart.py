from sqlalchemy import Column, String, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from ..base import Base


class ProductCartModel(Base):
    __tablename__ = "products_cart"
    __table_args__ = (PrimaryKeyConstraint("cart_id", "product_id"),)

    quantity = Column(Integer, nullable=False)
    cart_id = Column(String, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("ProductModel", uselist=False)
