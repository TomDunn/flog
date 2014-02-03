from os import environ

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(environ['POSTGRES_CONN'], echo = False)

Session = sessionmaker(bind=engine)
Base    = declarative_base()
