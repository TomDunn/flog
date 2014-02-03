from flask.ext.login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy import Sequence
from werkzeug.security import generate_password_hash, check_password_hash

from db import Base
from models.util.time_util import now
from models.util.session import add_and_refresh

class Author(Base, UserMixin):
    __tablename__ = 'authors'

    id    = Column(Integer, Sequence('users_seq'), unique=True, primary_key=True)
    email = Column(String, unique=True, primary_key=True)

    first_name = Column(String)
    last_name  = Column(String)

    # create and last modifed unix timestamps
    created  = Column(Float)
    modified = Column(Float)

    pw_hash = Column(String)

    @classmethod
    def create(cls, email, passwd, first_name, last_name, sync=True, session=None):
        author = cls()

        author.email  = email
        author.set_passwd(passwd)

        author.first_name = first_name
        author.last_name  = last_name

        author.created  = now()
        author.modified = now()

        if sync:
            add_and_refresh(session, author)

        return author

    def set_passwd(self, passwd):
        self.pw_hash = generate_password_hash(passwd)

    def check_passwd(self, passwd):
        return check_password_hash(self.pw_hash, passwd)
