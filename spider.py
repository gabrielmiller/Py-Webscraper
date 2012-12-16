import requests
import urlparse
import itertools
import re
from robotparser import RobotFileParser
from BeautifulSoup import BeautifulSoup
from time import sleep
from copy import deepcopy
from pymongo import Connection
from pymongo.errors import ConnectionFailure

REQUEST_TIME_INCREMENT = 5
SPIDER_USER_AGENT = 'Toastie'
PAGERANK_ITERATIONS = 30
PAGERANK_DAMPING = 0.85

max_hops = 0
max_frontiers = 0
max_pages = None

url_list, black_list, domain_robot_rules = [], [], {}

class Database():
    """
    Initiates a database connection and sets up data insertion/querying
    """

    def connect():
        """
        Establishes a database connection
        """
        try:
            connection = Connection(host="localhost", port=27017)
        except ConnectionFailure, error:
            return "Could not connect to database: %s" % error
            #sys.exit(1)
        self.dbc = connection["ex14"]

    def set_user_doc(doc):
        """
        Record the document to that was passed in as a dictionary
        """
        self.user_doc = doc

    def insert_doc():
        """
        Insert the document into the database
        """
        if self.user_doc & self.dbc:
            dbc.scrapedata.insert(self.user_doc, safe=True)

class Webpage():
    """
    Objects that refer to individual webpages. If the url is scrapeable the
    object will be filled with that data and inserted into a database for
    searching.
    """
    _instanceID = itertools.count(0)

    def __init__(self):
        """
        On initialization of a new url a count is added to the object
        """
        self.count = self._instanceID.next()

    def set_url(self, url):
        """
        A URL is passed in and the object's property url is set. If the URL
        has already been scanned or is blacklisted then the object is flagged
        to not be scanned.
        """
        #global url_list
        self.url = url
        if self.url not in url_list and self.url not in black_list:
            self.need_to_be_scanned = True
        else:
            self.need_to_be_scanned = False

    def page_robot_scannable(self):
        """
        Checks whether the page is allowed to be crawled
        """
        if self.needs_to_be_scanned is True:
            headers = {'User-agent':SPIDER_USER_AGENT}
            self.urlparse = urlparse.urlparse(self.url)
            robotcheck = RobotFileParser()
            robotcheck.set_url(urlparse)
            self.needs_to_be_scanned = robotcheck.can_fetch(SPIDER_USER_AGENT, self.urlparse[0]+'/robots.txt')

    def get_page(self):
        """
        The url is requested with a GET request. The page html is scraped
        directly, while elements of it are scraped in parse_page
        """
        headers = {'User-agent':SPIDER_USER_AGENT}
        try:
            self.request = requests.get(self.url, headers=headers)
            self.pagehtml = BeautifulSoup(self.request.text)
        except:
            raise Exception

    def get_visible_elements(self, element):
        """
        Checks that the element is not contained in <style>, <script>, <head>,
        <title> or [document]. It also cannot be commented out.
        """
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element)):
            return False
        return True

    def parse_page(self):
        """
        This method parses the HTML page and extracts the title of the page,
        the outgoing links, the number of outgoing links, and the text.
        """
        self.title = self.pagehtml.find('title').text
        self.page_text = self.pagehtml.findAll(text=true)

        for item in filter(get_visible_elements, self.pagetext):
            if item != '\n':
                self.pagetext+= item
        self.pagelinks = {}

        for link in soup.findAll('a'):
            self.pagelinks[link.get('href')] = 1

        for link in self.pagehtml:
            pass

        # determine if link is relative or absolute. if relative, change it to absolute

        # determine if link can be acquired by checking robots.txt
        # if it cannot be acquired, throw out the url

    def reverse_index_page_text(self):
        """
        Iterates through the words in the page text and creates and adds them
        to an index.
        """
        # This might take a really long time
        pass

    def set_page_scanned(self):
        """
        Once the page is scanned it is flagged as such
        """
        self.needs_to_be_scanned = False

def outgoing_links_to_pagerank(dictionary_of_outgoing_links):
    pagerank = {}
    for item in dictionary_of_outgoing_links:
        for outgoing_url in dictionary_of_outgoing_links[item]:
            if not pagerank.get(outgoing_url):
                pagerank[outgoing_url] = {}
                pagerank[outgoing_url]['pagerank'] = 1
                pagerank[outgoing_url]['incoming links'] = []
            pagerank[outgoing_url]['incoming links'].append(item)
    for item in pagerank:
        pagerank[item]['number of outgoing links'] = len(dictionary_of_outgoing_links[item])
    return pagerank

def page_rank(crawled_sites_incoming_link_format, number_of_iterations):
    """
    Iterates through the crawled webpages and ranks them based on their link
    structures.
    """
    i = number_of_iterations
    pagerank = crawled_sites_incoming_link_format
    while i is not 0:
        i-=1
        pagerankprev = deepcopy(pagerank)
        for item in pagerank:
            subeqn = 0
            for subitem, index in enumerate(pagerankprev[item]['incoming links']):
                subeqn += float(pagerankprev[pagerankprev[item]['incoming links'][subitem][0]]['pagerank']) / float(pagerankprev[pagerankprev[item]['incoming links'][subitem][0]]['outgoing links'])
            pagerank[item]['pagerank'] = (1-PAGERANK_DAMPING)+subeqn*(PAGERANK_DAMPING)
    pagerankprev = {}
    for item in pagerank:
        pagerankprev[item] = pagerank[item]['pagerank']
    return pagerankprev

def main():
    pass
    # Take the provided seed, frontiers, and maxpages and instantiate them
    seed = None
    frontiers = None
    maxpages = None
    firstseed = 0
    url_list.append(firstseed)

    for item in url_list:
        item = Webpage()
        item.set_url(url=seed)
        item.page_robot_scannable()
        if item.need_to_be_scanned is True:
            item.get_page()
            item.parse_parge()
            item.reverse_index_page()
            item.set_page_scanned()
        else:
            item.set_page_scanned()
        sleep(REQUEST_TIME_INCREMENT)

    dictionary_of_outgoing_links = {}

    for item in url_list:
        if item.pagehtml:
            dictionary_of_outgoing_links[item.url] = item.pagelinks

    page_rank(outgoing_links_to_pagerank(dictionary_of_outgoing_links), PAGERANK_ITERATIONS)

    # Connect to database, submit records for each webpage: url, title, pagehtml, pagetext, outgoinglinks, num_outgoinglinks, incominglinks
    # Submit reverse index data to database

    """

    URLDir.append((URL(seedURL),NULL,0))
    linkCache.append(seedURL,NULL)

    def process_url(input):
        input.getPage()
        if "error" not in dir(input):
            input.parsePage()
        #time.sleep(1)
        #Consider pulling time interval from robots.txt
        print "hop="+str(input.hop), "instance="+str(input), "len(URLDir)="+str(len(URLDir)), "URL="+input.URL

    for index, item in enumerate(URLDir):
        if urlparse.urlparse(item.url)[1] != "buttbox:8002":   #local testing
            continue
        if (index > maxFrontiers):
            break
        if (item.hop > maxHops):
            break
        print "Page "+str(index),
        process_url(item)
    """

if __name__ == "__main__":
    main()
