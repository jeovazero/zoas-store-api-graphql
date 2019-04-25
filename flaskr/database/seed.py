from .models import ProductModel, PhotoModel
from .base import Session, engine, Base

sticker = (
    "https://res.cloudinary.com/sohdezoas"
    "/image/upload/v1556136755/zoas/Group_14_mgkzzl.png"
)
book1 = (
    "https://res.cloudinary.com/sohdezoas"
    "/image/upload/v1556135859/zoas/Group_8_rfakg9.png"
)
book2 = (
    "https://res.cloudinary.com/sohdezoas"
    "/image/upload/v1556135845/zoas/Group_9_w0aim1.png"
)
mousepad11 = (
    "https://res.cloudinary.com/sohdezoas"
    "/image/upload/v1556136755/zoas/Group_11_egcx5s.png"
)
mousepad12 = (
    "https://res.cloudinary.com/sohdezoas"
    "/image/upload/v1556136756/zoas/Group_10_wntc1r.png"
)
mousepad2 = (
    "https://res.cloudinary.com/sohdezoas"
    "/image/upload/v1556136763/zoas/Group_13_viqda0.png"
)


def seed():
    print("SEED DB")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    photosSticker = [PhotoModel(sticker)]
    photosBook = [PhotoModel(book1), PhotoModel(book2)]
    photosMousepad1 = [PhotoModel(mousepad11), PhotoModel(mousepad12)]
    photosMousepad2 = [PhotoModel(mousepad2)]

    products = [
        ProductModel(
            title="Zoas Sticker",
            price=2.00,
            description="A sticker of zoas trademark",
            avaliable=50,
            avaliability=True,
            photos=photosSticker,
        ),
        ProductModel(
            title="Zoas Agenda",
            price=12.88,
            description="An agenda of zoas trademark",
            avaliable=20,
            avaliability=True,
            photos=photosBook,
        ),
        ProductModel(
            title="Zoas Mousepad Model 1",
            price=30.75,
            description="A Mousepad of zoas trademark",
            avaliable=11,
            avaliability=True,
            photos=photosMousepad1,
        ),
        ProductModel(
            title="Zoas Mousepad Model 2",
            price=30.70,
            description="A Mousepad of zoas trademark",
            avaliable=9,
            avaliability=True,
            photos=photosMousepad2,
        ),
    ]

    for product in products:
        Session.add(product)
        for photo in product.photos:
            Session.add(photo)

    Session.commit()
