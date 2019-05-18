from flask import session
import uuid


class SessionMixin:
    @classmethod
    def sid(cls):
        return str(session["u"])

    @classmethod
    def create_session(cls):
        session["u"] = uuid.uuid4()

    @classmethod
    def delete_session(cls):
        session.pop("u", None)
