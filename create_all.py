from db import Base, engine, Session
from models.Author import *
from models.Post import *

if __name__ == '__main__':
    Base.metadata.create_all(engine)

