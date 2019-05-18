import uuid
import base64
from flaskr.database import CartController
import re
import ast


def new_uuid():
    return str(uuid.uuid4())


def encode_base64(s):
    return base64.b64encode(s.encode("ascii")).decode("ascii")


def decode_base64(s):
    return base64.b64decode(s.encode("ascii")).decode("ascii")


def get_cookie(response):
    return response.headers["Set-Cookie"]


def get_session(response):
    cookie = get_cookie(response)
    return cookie.split(";")[0].split("=")


def get_cart_id(session):
    session_id = session.split(".")[0]

    # add padding
    session_id += "=" * ((4 - len(session_id) % 4) % 4)

    # decode
    session_decoded = decode_base64(session_id)

    # to dict
    session_dict = ast.literal_eval(session_decoded)

    # get cart id
    raw = session_dict["u"][" u"]
    m = re.match("(\\w{8})(\\w{4})(\\w{4})(\\w{4})(\\w{12})", raw)
    cart_id = "-".join(str(i) for i in m.groups())

    return cart_id


def add_fake_cart(client):
    session_id = str(new_uuid())
    CartController.create(id=session_id)
    with client.session_transaction() as session:
        session["u"] = session_id
    return session_id


def add_fake_cart_products(client):
    cart_id = add_fake_cart(client)
    CartController.add_product(id=cart_id, pid="2", quantity=11)
    CartController.add_product(id=cart_id, pid="1", quantity=20)
    return cart_id
