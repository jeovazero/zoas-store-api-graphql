from shirt import Shirt
from base import Session, engine


session = Session()
Shirt.__table__.drop(engine)


session.commit()
session.close()
