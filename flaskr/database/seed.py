from .models import ProductModel, PhotoModel
from .base import Session, engine, Base
import json
from os import path

SEED_FOLDER = path.dirname(path.abspath(__file__))
data_filename = path.join(SEED_FOLDER, "seed.data.json")


def to_product_model(product):
    photos = [PhotoModel(url) for url in product["photos"]]
    return ProductModel(
        title=product["title"],
        price=product["price"],
        description=product["description"],
        avaliable=product["avaliable"],
        avaliability=product["avaliability"],
        photos=photos,
    )


def seed():
    print("SEED DB")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with open(data_filename) as data:
        products_data = json.load(data)

    products = [to_product_model(p) for p in products_data]

    for product in products:
        Session.add(product)
        for photo in product.photos:
            Session.add(photo)

    Session.commit()
