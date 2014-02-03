import unittest

from models.Author import Author
from models.tests.base import BaseTest

class TestUser(BaseTest):

    def test_create(self):
        author = Author.create('test@test.com', 'testing123', 'john', 'q', session=self.session)

        self.assertTrue(author.email == 'test@test.com')
        self.assertTrue(author.first_name == 'john')
        self.assertTrue(author.last_name == 'q')
        self.assertTrue(author.pw_hash is not None)
        self.assertTrue(author.check_passwd('testing123'))
        self.assertTrue(not author.check_passwd('foooop'))

if __name__ == '__main__':
    unittest.main()
