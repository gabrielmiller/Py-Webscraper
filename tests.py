import unittest
from random import randint
from spider import *

"""
This module will include all of the unit tests
"""

class SpiderTests(unittest.TestCase):
    """
    This test suite contains tests on the functionality provided by the spider
    module.
    """

    def setUp(self):
        """
        Sets the environment for testing the spider
        """
        pass

    def test_blarg(self):
        """
        Tests if the spider will
        """
        self.assertEqual(self.blah, bler), "self.blah is not equal to bler"
        pass

    def tearDown(self):
        """
        Closes the environment for testing the spider
        """
        pass

if __name__ == "__main__":
    unittest.main()
