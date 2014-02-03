import re

from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Sequence

from db import Base
from models.Author import Author
from models.util.time_util import now
from models.util.session import add_and_refresh

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, Sequence('posts_seq'), unique=True, primary_key=True)

    author_id = Column(Integer, ForeignKey('authors.id'))
    author    = relationship('Author')

    created  = Column(Float)
    modified = Column(Float)

    title = Column(String)
    slug  = Column(String)

    body = Column(String)

    status = Column(String)

    STATUSES = frozenset(['PRIVATE_DRAFT', 'DRAFT', 'RELEASED'])

    @classmethod
    def create(cls, author, title=None, body=None, sync=False, session=None):
        post = cls()
        #post.author_id = author.id

        time = now()
        post.created  = time
        post.modified = time

        if body is None:
            post.body = '<p>no content yet</p>'

        if title is None:
            post.set_title("Post created at %s" % str(time))

        if sync is True and session is not None:
            add_and_refresh(session, post)

        return post

    def set_title(self, title):
        self.title = title
        self.slug  = re.sub('[^0-9a-zA-Z]+', '-', title)
