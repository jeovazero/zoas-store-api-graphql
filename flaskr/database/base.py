from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os

DB = os.environ["POSTGRES_DB"]
USER = os.environ["POSTGRES_USER"]
PASSWORD = os.environ["POSTGRES_PASSWORD"]
PORT = os.getenv("POSTGRES_PORT", 5432)
HOST = os.getenv("POSTGRES_HOST", "localhost")

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")
Session = scoped_session(
    sessionmaker(bind=engine, autocommit=False, autoflush=False)
)
Base = declarative_base()
Base.query = Session.query_property()
