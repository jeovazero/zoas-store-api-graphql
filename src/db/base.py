from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine("postgresql://yornero:yornero@localhost:5432/zoas-store")
Session = scoped_session(
    sessionmaker(bind=engine, autocommit=False, autoflush=False)
)
Base = declarative_base()
Base.query = Session.query_property()
