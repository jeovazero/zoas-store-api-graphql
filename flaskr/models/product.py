from .alias import Base, Column, Integer, String, Float, Boolean, relationship


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    avaliable = Column(Integer, nullable=False)
    avaliability = Column(Boolean, nullable=False)
    photos = relationship("PhotoModel", backref="product")
