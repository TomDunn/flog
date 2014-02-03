import unittest

from db import Base, engine, Session
from models.Author import Author

class BaseTest(unittest.TestCase):
    """
    Base data model test
    responsible for set up and tear down
    """

    def setUp(self):
        self.session = Session()
        self.engine  = engine

        Base.metadata.create_all(self.engine)

    def tearDown(self):
        self.session.close()
        Base.metadata.drop_all(self.engine)
