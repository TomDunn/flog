import unittest

from models.Post import Post
from models.tests.base import BaseTest

class TestPost(BaseTest):

    def test_create(self):
        post = Post()



if __name__ == '__main__':
    unittest.main()
