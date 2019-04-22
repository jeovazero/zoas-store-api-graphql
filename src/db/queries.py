from base import Session
from shirt import ShirtModel


session = Session()


shirts = session.query(ShirtModel).all()


print("#Shirts here")
for shirt in shirts:
    print(f"Shirt {shirt.title}: R${shirt.price}")

print("#############\n")
