import os


class Base(object):
    # GENERAL
    DEBUG = False
    TESTING = False
    ENV = os.getenv("FLASK_ENV", "production")

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

    # SESSION
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "W1r+xoQVRHUeQowoaPysNq6vO3badR1tOPTHwlA46rZKSVLjok8jiG3ue3vE3VU2G/M=",
    )
    SESSION_COOKIE_NAME = "80l4ch4"

    # DATABASE
    DB = os.environ["POSTGRES_DB"]
    USER = os.environ["POSTGRES_USER"]
    PASSWORD = os.environ["POSTGRES_PASSWORD"]
    PORT = os.getenv("POSTGRES_PORT", 5432)
    HOST = os.getenv("POSTGRES_HOST", "localhost")
    DB_URI = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(Base):
    pass


class Development(Base):
    DEBUG = True
    ENV = "development"


class Testing(Base):
    TESTING = True
