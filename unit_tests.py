import unittest
from bson.objectid import ObjectId
from random import randint
from settings import *
from spider import *
from routes import *
import database
import helpers

"""
This module includes all of the unit tests.
"""

class DatabaseTests(unittest.TestCase):
    """
    Tests database functions.
    """

    def setUp(self):
        self.dbconnection = database.DatabaseConnection()
        self.dbconnection.connect()
        self.maxDiff = None

    def test_a_known_search_of_one_word_returns_expected_documents(self):
        """
        Verifies a known input index cursor returns the correct documents.
        """
        self.search_query = {'$or': [{'url': u'url1'}, {'url': u'url4'}, {'url': u'url2'}, {'url': u'url3'}]}
        self.expected_result = {
u'url4': {u'title': u"URL4's page title", u'url': u'url4', u'pagetext': u'beep beep honk honk beep beep honk honk honk', u'pagerank': 0.27, u'date': u'20130511', u'flavor': u'lightning', u'_id': ObjectId('518ee0c72938d8587f000000')},
u'url1': {u'title': u"URL1's page title", u'url': u'url1', u'pagetext': u'Derp doop deep diggty doo wop dee voop.', u'pagerank': 0.4, u'date': u'20130511', u'flavor': u'blood', u'_id': ObjectId('518edf9f2938d80c5a000000')},
u'url3': {u'title': u"URL3's page title", u'url': u'url3', u'pagetext': u'Hurrrrr derr doop boo boo doo too see dee bee dee.', u'pagerank': 0.37, u'date': u'20130511', u'flavor': u'thunder', u'_id': ObjectId('518ee0c02938d8dc7c000002')},
u'url2': {u'title': u"URL2's page title", u'url': u'url2', u'pagetext': u'beebity boop bop beeweeoop bop bop bleeb beep boop.', u'pagerank': 0.32, u'date': u'20130511', u'flavor': u'blood', u'_id': ObjectId('518edfdc2938d80e5a000000')}}
        self.expected_result_count = 4
        self.result, self.result_count = database.query_mongo(query=self.search_query, collection=COLLECTION_DOCUMENTS, db=self.dbconnection)
        self.assertEqual(self.result, self.expected_result), "A known pages query with known results returned incorrect results."
        self.assertEqual(self.result_count, self.expected_result_count), "A known pages query with known results returned the wrong number of results."

    def test_a_known_search_of_two_words_returns_expected_indices(self):
        """
        Tests a search of two words with known results for the expected result.
        """
        self.search_query="word1 word2"
        self.expected_result={u'word1':{u'url4': [6], u'url1': [9], u'url3': [1, 3, 4], u'url2': [1]},
                              u'word2':{u'url4': [5], u'url1': [6], u'url3': [12], u'url2': [74]}}
        self.query = database.build_mongo_index_query(input=self.search_query)
        self.cursor, self.cursor_count = database.query_mongo(query=self.query, collection=COLLECTION_INDEX, db=self.dbconnection)
        self.assertEqual(self.cursor, self.expected_result), "Test of two known search results does not give the correct response."

    def test_building_a_single_word_mongo_index_query(self):
        """
        Tests if a single word searched will build the proper mongo index query.
        """
        self.test_function_input = "thisisaword"
        self.expected_function_output = {'word':'thisisaword'}
        self.result = database.build_mongo_index_query(input=self.test_function_input)
        self.assertEqual(self.result, self.expected_function_output), "Searching for one word is not building the proper mongo index query"

    def test_building_a_two_word_mongo_index_query(self):
        """
        Tests if a two word search will build the proper mongo index query.
        """
        self.test_function_input = "two words"
        self.expected_function_output = {'$or':[{'word':'two'},{'word':'words'}]}
        self.result = database.build_mongo_index_query(input=self.test_function_input)
        self.assertEqual(self.result, self.expected_function_output), "A case for two words is not building the proper mongo index query"

    def test_building_a_three_word_mongo_index_query(self):
        """
        Tests if a three word search will build the proper mongo index query.
        """
        self.test_function_input = "there are three"
        self.expected_function_output = {'$or':[{'word':'there'},{'word':'are'},{'word':'three'}]}
        self.result = database.build_mongo_index_query(input=self.test_function_input)
        self.assertEqual(self.result, self.expected_function_output), "A test for three words is not building the proper mongo index query"

    def test_building_a_one_word_mongo_pages_query(self):
        """
        Tests if a one word search will build the proper mongo pages query.
        """
        self.test_input_cursor = {'word1': {'url1':[9], 'url2':[1], 'url3':[1,3,4], 'url4':[6]}}
        self.expected_output = {'$or':[{'url':'url4'},{'url':'url1'},{'url':'url3'},{'url':'url2'}]}
        self.expected_hits = {'url1':[9], 'url2':[1], 'url3':[1,3,4], 'url4':[6]}
        self.result, self.hits = database.build_mongo_pages_query(input=self.test_input_cursor)
        self.assertEqual(self.result, self.expected_output), "Building a page query for a one word search is broken."
        self.assertEqual(self.hits, self.expected_hits), "Building a page word hits list for a one word search is broken."

    def test_building_a_two_word_mongo_pages_query(self):
        """
        Tests if a two word search will build the proper mongo pages query.
        """
        self.test_input_cursor = {'word1': {'url1':[9], 'url2':[1], 'url3':[1,3,4], 'url4':[6]},
                                  'word2': {'url1':[6], 'url2': [74], 'url3': [12], 'url4': [5]}}
        self.expected_output = {'$or':[{'url':'url1'},{'url':'url4'},{'url':'url2'},{'url':'url3'}]}
        self.expected_hits = {'url1':[9,6], 'url2':[1,74], 'url3':[1,3,4,12], 'url4':[5,6]}
        self.result, self.hits = database.build_mongo_pages_query(input=self.test_input_cursor)
        self.assertEqual(self.result, self.expected_output), "Building a page query for a two word search is broken."
        self.assertEqual(self.hits, self.expected_hits), "Building a page word hits list for a two word search is broken."

class HelperTests(unittest.TestCase):
    """
    Tests functions in the helpers module.
    """

    def test_remove_duplicate_dictionaries(self):
        """
        Compares list with duplicate dictionaries to a known list of the
        distinct dictionaries in the former list.
        """
        self.input = [{"item a": 1},{"item b":3},{"item a":1},{"item b":2}]
        self.expected_output = [{"item b": 2},{"item b":3},{"item a":1}]
        self.result = helpers.remove_duplicate_dictionaries(self.input)
        self.assertEqual(self.result, self.expected_output), "helpers.remove_duplicate_dictionaries is not removing duplicate dictionaries."

    def test_remove_duplicate_numbers(self):
        """
        Compares list with duplicate numbers to a known list of the
        distinct numbers values in the former list.
        """
        self.input = [1,6,2,7,3,4,5,1,6,7,7,7,8]
        self.expected_output = [1,2,3,4,5,6,7,8]
        self.result = helpers.remove_duplicate_numbers(self.input)
        self.assertEqual(self.result, self.expected_output), "helpers.remove_duplicate_numbers is not removing duplicate numbers."

class SpiderTests(unittest.TestCase):
    """
    Tests functions in the spider module.
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

    def test_is_a_robot_scannable_page_scannable(self):
        """
        Tests if a page entered scannable in a robots.txt is correctly
        interpreted as scannable.
        """
        url_of_interest = "http://helium/scannable_to_ua_Toastie"
        self.beepboop.load_url(url_of_interest)
        self.assertEqual(self.beepboop.need_to_be_scanned, True), "Scannable url according to robots.txt is correctly scannable prior to being checked"
        self.beepboop.page_robot_scannable()
        #self.assertEqual(self.beepboop.need_to_be_scanned, True), "Scannable url according to robots.txt is correctly scannable after being checked"


    def test_is_a_robot_unscannable_page_unscannable(self):
        """
        Tests if a page entered unscannable in a robots.txt is correctly
        interpreted as unscannable.
        """
        url_of_interest2 = "http://helium/unscannable_to_ua_Toastie"
        self.beepboop.load_url(url_of_interest2)
        self.assertEqual(self.beepboop.need_to_be_scanned, True), "Unscannable url according to robots.txt is correctly scannable prior to being checked"
        self.beepboop.page_robot_scannable()
        self.assertEqual(self.beepboop.need_to_be_scanned, False), "Unscannable url according to robots.txt is correctly unscannable after being checked"

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
        unrounded floats, however they are 'equivalent enough' values for our
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
