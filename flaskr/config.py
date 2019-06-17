import os


class Base(object):
    DEBUG = False
    TESTING = False
    ENV = os.getenv("FLASK_ENV", "production")

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "W1r+xoQVRHUeQowoaPysNq6vO3badR1tOPTHwlA46rZKSVLjok8jiG3ue3vE3VU2G/M=",
    )
    SESSION_COOKIE_NAME = "80l4ch4"


class Production(Base):
    pass


class Development(Base):
    DEBUG = True
    ENV = "development"


class Testing(Base):
    TESTING = True
