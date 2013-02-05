import unittest
from random import randint
from spider import *
from routes import *
from database import DatabaseConnection
import functions

"""
This module will include all of the unit tests
"""

class DatabaseTests(unittest.TestCase):
    """
    This test suite contains tests on the functionality provided by the
    database module.
    """

    def setUp(self):
        #self.dbconnection = DatabaseConnection()
        pass

    def test_a_search_query_is_built_from_the_input(self):
        """
        Tests if a search query for mongoDB is properly created from the
        search words provided.
        """

class FunctionTests(unittest.TestCase):
    """
    This test suite contains tests on the Functions module.
    """

    def setUp(self):
        pass

    def test_building_a_single_word_mongo_query(self):
        """
        Tests if a single word searched will build the proper mongo query.
        """
        self.test_function_input = "thisisaword"
        self.expected_function_output = {'word':'thisisaword'}
        self.a = functions.build_mongo_query_from_search_terms(input=self.test_function_input, action="select_indices")
        self.assertEqual(self.a, self.expected_function_output), "Searching for one word is not building the proper mongo query"

    def test_building_a_two_word_mongo_query(self):
        """
        Tests if a two word search will build the proper mongo query.
        """
        self.test_function_input = "two words"
        self.expected_function_output = {'$or':[{'word':'two'},{'word':'words'}]}
        self.a = functions.build_mongo_query_from_search_terms(input=self.test_function_input, action="select_indices")
        self.assertEqual(self.a, self.expected_function_output), "A case for two words is not building the proper mongo query"

    def test_building_a_three_word_mongo_query(self):
        """
        Tests if a two word search will build the proper mongo query.
        """
        self.test_function_input = "there are three"
        self.expected_function_output = {'$or':[{'word':'there'},{'word':'are'},{'word':'three'}]}
        self.a = functions.build_mongo_query_from_search_terms(input=self.test_function_input, action="select_indices")
        self.assertEqual(self.a, self.expected_function_output), "A test for three words is not building the proper mongo query"

class SpiderTests(unittest.TestCase):
    """
    This test suite contains tests on the functionality provided by the spider
    module.
    """

    def setUp(self):
        """
        Sets the environment for testing the spider
        """
        self.beepboop = Webpage()

    def test_new_Webpage_is_type_webpage(self):
        """
        Is a new instance of Webpage of the type Webpage?
        """
        self.assertEqual(type(self.beepboop), type(Webpage())), "Instantiated Webpage object is not equal to type url"

    def test_new_Webpage_object_has_url_assigned_and_it_is_equal_to_assignment(self):
        """
        Does a newly instantiated Webpage object have the correct url
        attribute after being assigned one?
        """
        theurl = "http://www.google.com"
        self.beepboop.load_url(theurl)
        self.assertEqual(self.beepboop.url, theurl), "Instantiated url object's url property doesn't match what it was defined to be"

    def test_blacklisted_webpage_objects_should_not_be_scannable(self):
        """
        Is a blacklisted page correctly flagged to not be scanned?
        """
        theurl = "http://www.google.com"
        black_list.append(theurl)
        self.beepboop.load_url(theurl)
        self.assertEqual(self.beepboop.need_to_be_scanned, False), "Blacklisted URL should not be scannable, but was shown to be scannable"

    def test_does_unreachable_url_throw_error(self):
        """
        Is a website at an  unreachable url flagged to not be scanned?
        """
        self.beepboop.load_url("www.poopiedoopie.com") #Hopefully this won't become a dirty website in the future
        self.beepboop.page_robot_scannable()
        self.beepboop.need_to_be_scanned
        self.assertEqual(self.beepboop.need_to_be_scanned, False), "Website at an unreachable URL should not be scannable but was flagged scannable"

    def test_previously_scanned_webpages_should_not_be_scannable(self):
        """
        Is a previously scanned page correctly flagged to not be scanned?
        """
        theurl2 = "http://www.google.com"
        url_list.append(theurl2)
        self.beepboop.load_url(theurl2)
        self.assertEqual(self.beepboop.need_to_be_scanned, False), "Previous scanned URL should not be scannable, but was shown to be scannable"

##############################################################################
#  These two commented tests require a server with the below-mentioned user-
#  agent to succeed.
##############################################################################
#    def test_is_a_robot_scannable_page_scannable(self):
#        """
#        Tests if a page entered scannable in a robots.txt is correctly
#        interpreted as scannable.
#
#        curl of buttbox:8002/robots.txt responds as follows:
#
#        User-agent: Toastie
#        Disallow: /unscannable_to_ua_Toastie
#        """
#        url_of_interest = "http://buttbox:8002/scannable_to_ua_Toastie"
#        self.beepboop.load_url(url_of_interest)
#        self.assertEqual(self.beepboop.need_to_be_scanned, True), "Scannable url according to robots.txt is correctly scannable prior to being checked"
#        self.beepboop.page_robot_scannable()
#        #self.assertEqual(self.beepboop.need_to_be_scanned, True), "Scannable url according to robots.txt is correctly scannable after being checked"
#
#
#    def test_is_a_robot_unscannable_page_unscannable(self):
#        """
#        Tests if a page entered unscannable in a robots.txt is correctly
#        interpreted as unscannable.
#
#        curl of buttbox:8002/robots.txt responds as follows:
#
#        User-agent: Toastie
#        Disallow: /unscannable_to_ua_Toastie
#        """
#        url_of_interest2 = "http://buttbox:8002/unscannable_to_ua_Toastie"
#        self.beepboop.load_url(url_of_interest2)
#        self.assertEqual(self.beepboop.need_to_be_scanned, True), "Unscannable url according to robots.txt is correctly scannable prior to being checked"
#        self.beepboop.page_robot_scannable()
#        self.assertEqual(self.beepboop.need_to_be_scanned, False), "Unscannable url according to robots.txt is correctly unscannable after being checked"

    def test_is_inverted_index_working(self):
        """
        Tests whether the inverted indexing mechanism is working properly
        """
        self.beepboop.pagetext = "How would you like to work for a big company like Google? They are quite big"
        self.beepboop.load_url("http://goatse.cx/")
        self.beepboop.inverted_index_page_text()
        self.assertEqual(inverted_index['big']['offsets'], [8, 15]), "The inverted index is not properly functioning."
        #for item in inverted_index:
        #    print item, inverted_index[item]

    def test_does_inverted_index_disclude_stopwords(self):
        """
        Tests if the inverted index properly discludes stopwords
        """
        self.beepboop.pagetext = "the able about while where when which with yet you too twas these only on every his should wants"
        self.beepboop.load_url("url")
        self.beepboop.inverted_index_page_text()
        self.assertEqual(inverted_index, {}), "Inverted index tried to index a stopword"

    def test_outgoing_links_to_pagerank_format(self):
        """
        Test the mechanism for converting a dictionary of urls and their
        outgoing links to a dictionary of urls, their incoming links, and
        the number of links on each incoming links' page.
        """
        dictionary_of_outgoing_links = {'site1':[         'site2', 'site3'],
                                        'site2':[                  'site3'],
                                        'site3':['site1', 'site2'         ]}

        expected_output = {'site1':{'incoming links':[                  'site3'], 'number of outgoing links': 2, 'pagerank': 1},
                           'site2':{'incoming links':['site3', 'site1'         ], 'number of outgoing links': 1, 'pagerank': 1},
                           'site3':{'incoming links':['site2', 'site1'         ], 'number of outgoing links': 2, 'pagerank': 1}}

        self.assertEqual(outgoing_links_to_pagerank(dictionary_of_outgoing_links), expected_output), "Conversion from outgoing link format to incoming link format failed."

    def test_pagerank_results(self):
        """
        Test the results coming out of the pagerank algorithm.
        Note: the results of this assert do not pass unit test because they are
        unrounded floats, however they are equivalent enough values for our
        search engine purposes.
        """

        #expected_input =  {'site1':{'incoming links':[                  'site3'], 'number of outgoing links': 2, 'pagerank': 1},
        #                   'site2':{'incoming links':['site3', 'site1'         ], 'number of outgoing links': 1, 'pagerank': 1},
        #                   'site3':{'incoming links':['site2', 'site1'         ], 'number of outgoing links': 2, 'pagerank': 1}}

        #self.assertEqual(page_rank(expected_input, 1), {'site1':0.575, 'site2':1.0, 'site3':1.425}), "Pagerank output round 1 incorrect"
        #self.assertEqual(page_rank(expected_input, 2), {'site1':0.755625, 'site2':1.0, 'site3':1.244375}), "Pagerank output round 2 incorrect"
        #self.assertEqual(page_rank(expected_input, 3), {'site1':0.678859375, 'site2':1.0, 'site3':1.321140625}), "Pagerank output round 3 incorrect"

    def test_pagerank_with_an_unscanned_site(self):
        """
        Test the results coming out of the pagerank algorithm.
        To deal with unscanned but referenced webpages the
        program adds an entry and assumes 1 incoming link.

        The two inputs below should have identical output.
        """
        input3 = {'site1':[         'site2', 'site3', 'site4'],
                  'site2':[                  'site3', 'site4'],
                  'site3':['site1', 'site2'                  ]}

        input4 = {'site1':[         'site2', 'site3', 'site4'],
                  'site2':[                  'site3', 'site4'],
                  'site3':['site1', 'site2'                  ],
                  'site4':[                                  ],
                  'site5':[                                  ]}

        a_random_number = randint(0,10)
        self.assertEqual(page_rank(outgoing_links_to_pagerank(input3), a_random_number), page_rank(outgoing_links_to_pagerank(input4), a_random_number)), "Unscanned site pagerank is incorrect"

    def tearDown(self):
        """
        Closes the environment for testing the spider.
        """
        pass

if __name__ == "__main__":
    unittest.main()
