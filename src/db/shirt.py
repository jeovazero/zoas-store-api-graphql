from sqlalchemy import Column, String, Integer, Float
from .base import Base


class ShirtModel(Base):
    __tablename__ = "shirts"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)

    def __init__(self, title: str, price: float) -> None:
        self.title = title
        self.price = price
