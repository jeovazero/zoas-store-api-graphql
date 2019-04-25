from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.orm import relationship
from ..base import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    avaliable = Column(Integer, nullable=False)
    avaliability = Column(Boolean, nullable=False)
    photos = relationship("PhotoModel", backref="product")
