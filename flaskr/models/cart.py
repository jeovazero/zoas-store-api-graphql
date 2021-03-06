from .alias import Base, Column, relationship, String


class CartModel(Base):
    __tablename__ = "carts"

    id = Column(String, primary_key=True)
    products = relationship(
        "ProductCartModel",
        backref="cart",
        cascade="delete",
        order_by="ProductCartModel.product_id",
    )
