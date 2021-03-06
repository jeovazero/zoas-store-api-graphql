from .alias import Base, Column, Integer, String, ForeignKey


class PhotoModel(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))

    def __init__(self, url: str) -> None:
        self.url = url
