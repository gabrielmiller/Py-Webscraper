import requests
import urlparse
import re
import settings
from robotparser import RobotFileParser
from time import sleep
from copy import deepcopy
from database import DatabaseConnection
from stopwords import STOP_WORDS

"""
Webpage scraping objects and methods
"""

class Webpage(object):
    """
    Objects that refer to individual webpages. If the url is scrapeable the
    object will be filled with that data, indexed, and inserted into a database
    to be searched.
    """

    scraped_pages = []

    def __init__(self, url):
        """
        Constructs a webpage object and assigns it the given url.
        """
        self.url = url
        self.get_object = None
        self.html = None
        self.urlparse = urlparse.urlparse(self.url)
        self.robots_txt = None

    def is_page_robot_scannable(self):
        """
        Returns a boolean that tells whether the page is robot scrapeable.
        """
        robotcheck = RobotFileParser()
        robotcheck.set_url(self.urlparse[0]+'://'+self.urlparse[1]+'/robots.txt')
        robotcheck.read()
        return robotcheck.can_fetch(settings.SPIDER_USER_AGENT, self.url)

    def is_page_scraped(self):
        """
        Returns a boolean that tells whether the page has been scraped.
        """
        return self.url in Webpage.scraped_pages

    def get_page(self):
        """
        Returns a GET request for the page.
        """
        pass

    def parse_page(self):
        """
        Parses html strings. Extracts page text and hrefs.
        """
        pass

    def create_inverted_index(self, parsed_text):
        """
        Returns an inverted index of the words in the provided text.
        """
        pass
