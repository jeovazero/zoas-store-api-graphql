from shirt import ShirtModel
from base import Session, engine, Base


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


shirts = [
    ShirtModel("Blue", 34.00),
    ShirtModel("Red", 92.00),
    ShirtModel("Green", 104.00),
]


for _shirt in shirts:
    Session.add(_shirt)

Session.commit()
