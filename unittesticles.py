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
        self.beepboop = URL()

    def test_new_URL_is_type_URL(self):
        """
        Is a new instance of URL of the type URL?
        """
        self.assertEqual(type(self.beepboop), type(URL())), "Instantiated url object is not equal to type url"

    def test_new_URL_object_has_url_assigned_and_it_is_equal_to_assignment(self):
        """
        """
        theurl = "http://www.google.com"
        self.beepboop.set_url(theurl)
        self.assertEqual(self.beepboop.url, theurl), "Instantiated url object's url property doesn't match what it was defined to be"

    def test_some_URL_objects_should_not_be_scannable(self):
        """
        Is a nonscannable page correctly noticed?
        """
        self.assertEqual(self.beepboop.needs_to_be_scanned, False), "URL should not be scannable, but was shown to be scannable"

    def tearDown(self):
        """
        Closes the environment for testing the spider
        """
        pass

if __name__ == "__main__":
    unittest.main()
