from .models import ProductModel, PhotoModel
import json
import click
from os import path
from flask import current_app
from flask.cli import with_appcontext
from flaskr import db

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


@click.command("seed-db")
@with_appcontext
def seed_command():
    db.init_app(current_app)
    db.drop_all()
    db.create_all()

    with open(data_filename) as data:
        products_data = json.load(data)

    products = [to_product_model(p) for p in products_data]

    for product in products:
        db.session.add(product)
        for photo in product.photos:
            db.session.add(photo)

    db.session.commit()
    print("seed Done!")
