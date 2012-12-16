import requests
import urlparse
import re
from robotparser import RobotFileParser
from BeautifulSoup import BeautifulSoup
from time import sleep
from copy import deepcopy
from pymongo import Connection
from pymongo.errors import ConnectionFailure
from stopwords import STOP_WORDS

REQUEST_TIME_INCREMENT = 5
SPIDER_USER_AGENT = 'Toastie'
PAGERANK_ITERATIONS = 30
PAGERANK_DAMPING = 0.85

url_list, black_list, inverted_index = [], [], {}

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
    number_of_scraped_pages = 0

    def load_url(self, url):
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
        if self.need_to_be_scanned is True:
            try:
                headers = {'User-agent':SPIDER_USER_AGENT}
                self.urlparse = urlparse.urlparse(self.url)
                self.robotcheck = RobotFileParser()
                self.robotcheck.set_url('http://'+self.urlparse[1]+'/robots.txt') # Only works with http right now.
                self.robotcheck.read()
                self.need_to_be_scanned = self.robotcheck.can_fetch(SPIDER_USER_AGENT, self.url)
            except:
                self.need_to_be_scanned = False

    def get_page(self):
        """
        The url is requested with a GET request. The page html is scraped
        directly, while elements of it aee scraped in parse_page
        """
        headers = {'User-agent':SPIDER_USER_AGENT}
        try:
            self.request = requests.get(self.url, headers=headers)
            self.pagehtml = BeautifulSoup(self.request.text)
            self.count = self.instanceID.next()
            Webpage.number_of_scraped_pages += 1
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

    def inverted_index_page_text(self):
        """
        Iterates through the words in the page text and creates and adds them
        to an index.
        """
        self.pagetextlist = self.pagetext.split(' ') #Noted error: This catches punctuation along with words.
        for index, word in enumerate(self.pagetextlist):
            if word not in STOP_WORDS:
                if not inverted_index.get(word):
                    inverted_index[word]={'url':self.url,'offsets':[index]}
                else:
                    inverted_index[word]['offsets'].append(index)

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
        try:
            pagerank[item]['number of outgoing links'] = len(dictionary_of_outgoing_links[item])
        except KeyError: #If a page was linked to but it was not scanned there will be a KeyError. This will fill in the "best known" information for that record.
            pagerank[item] = {'number of outgoing links': 0, 'incoming links':[]}
            for subitem in pagerank:
                try:
                    if item in dictionary_of_outgoing_links[subitem]:
                        pagerank[item]['incoming links'].append(subitem)
                        pagerank[item]['number of outgoing links']+=1
                except:
                    pass
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
            # For each url of an incoming site, that site is traversed for its pagerank and number of outgoing links
            # The iteration below runs once for every incoming url to a page(one for every arrow head in a graph)
            for index, subitem in enumerate(pagerankprev[item]['incoming links']):
                subeqn += float(pagerankprev[pagerankprev[item]['incoming links'][index]]['pagerank']) / float(pagerankprev[pagerankprev[item]['incoming links'][index]]['number of outgoing links'])
            pagerank[item]['pagerank'] = (1-PAGERANK_DAMPING)+subeqn*(PAGERANK_DAMPING)
    pagerankprev = {}
    for item in pagerank:
        pagerankprev[item] = pagerank[item]['pagerank']
    return pagerankprev

def main():
    # Take the provided seed, max frontiers, max hops, and max pages and 
    # instantiate them
    # Will implement frontiers and hops in a later revision
    seed = None
    max_pages = None
    firstseed = 0
    url_list.append(firstseed)

    for item in url_list:
        if len(Webpage.instanceID) > maxpages:
            break
        #if frontier > max_frontiers:
        #    break
        #if hop > max_hops:
        #    break
        item = Webpage()
        item.load_url(url=seed)
        item.page_robot_scannable()
        if item.need_to_be_scanned is True:
            item.get_page()
            item.parse_parge()
            item.inverted_index_page()
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
    # Submit inverted index data to database

if __name__ == "__main__":
    main()
