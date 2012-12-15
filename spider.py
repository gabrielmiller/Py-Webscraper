import requests
import BeautifulSoup
import urlparse
import itertools
import re
import robotparser
from pymongo import Connection
from pymongo.errors import ConnectionFailure

REQUEST_TIME_INCREMENT = 5
SPIDER_USER_AGENT = 'Toastie'
PAGERANK_ITERATIONS = 30
PAGERANK_DAMPING = 0.85

max_hops = 0
max_frontiers = 0
max_pages = None

url_list, link_cache, black_list = [], {}, []

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
            pass

        headers = {'User-agent':SPIDER_USER_AGENT}
        #check robots. If robots says no scanning, throw out page
        #robotcheck = requests.get(urlparse.urlparse(URL)[1]+/robots.txt')

    def get_page(self):
        """
        The url is requested with a GET request if it hasn't yet been
        """
        #global SPIDER_USER_AGENT

        #testing
        if urlparse.urlparse(self.url)[1] in whitelist:
            self.request = requests.get(url, headers=headers)
            self.soup = BeautifulSoup.BeautifulSoup(self.request.text)
        else:
            self.error = True

    def get_visible_elements(element):
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
        self.title = self.soup.find('title').text
        self.text = self.soup.findAll(text=true)
        self.pageText = ''

        for item in filter(get_visible_elements, self.text):
            if item != '\n':
                visibleText+= item
        self.pagelinks = []

        for link in soup.findAll('a'):
            self.pagelinks.append(link.get('href'))
        self.pagelinks.sort()

        for link in self.pagelinks:
            self.lastitem = self.pagelinks[-1]
            #determine if link is a duplicate of the previous. if so, throw it out.
            for i in range(len(self.pagelinks) - 2, -1, -1):
                if self.lastitem == self.pagelinks[i]:
                    del self.pagelinks[i]
                else:
                    self.lastitem = self.pagelinks[i]

            #determine if link is relative or absolute. if relative, change it to absolute

            #determine if link can be acquired by checking robots.txt
            #if it cannot be acquired, throw out the url

            if link in linkCache:
                if link in linkCache[self.url]:
                    pass
                else:
                    linkCache[self.url].append(link)
            else:
                url_list.append(link)
                linkCache[self.url]=[link]

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
            pagerank[outgoing_url]['incoming links'].append((item, len(dictionary_of_outgoing_links[item])))
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
        for item in pagerank:
            subeqn = 0
            for subitem in pagerank[item]['incoming links']:
                subeqn += pagerank[pagerank[item]['incoming links'][0][0]]['pagerank'] / pagerank[item]['incoming links'][0][1]
            pagerank[item]['pagerank'] = (1-PAGERANK_DAMPING) + (PAGERANK_DAMPING * subeqn)
    return pagerank

    """
    for item in expected_input:
        print item, '0.15 + 0.85 * (',
        for subitem in expected_input[item]['incoming links']:
            print '(', expected_input[expected_input[item]['incoming links'][0][0]]['pagerank'],'/',expected_input[item]['incoming links'][0][1],') +',
        print ') \n'
    """

    """
        for twotuple in pagerank[item]:
            if not pagerank_output.get(item[0]): #First iteration of pagerank
                pagerank_output[item[0]] = (1-PAGERANK_DAMPING) * ((PAGERANK_DAMPING))
            else: #Subsequent iterations of pagerank
                pagerank_output[item[0]] = 0 ###
    """

def main():
    while 1:
        input = raw_input("Enter a seed url >> ")
        """
        try:
            if (type(input) == str) & (input[:7] == "http://"):
                break
            else:
                print "Your input must be a string that begins with http://"
        except IndexError: #in case input was left blank
            print "Your input must be a string that begins with http://"
        except:
            print "An unexpected error occurred. Please try again. \nYour input must be a string that begins with http://"
        """

        input = "http://127.0.0.1/~batman/"
        #input = "http://buttbox:8002/~gabe/"
        break
    seedURL = input[:]

    while 1:
        input = raw_input("Enter a maximum number of webpages to crawl >> ")
        try:
            if (int(input) > 0):
                break
            else:
                print "You must enter a number greater than 0"
        except:
            print "You must enter a number greater than 0"

    maxFrontiers = int(input)

    while 1:
        input = raw_input("Enter a maximum number of links beyond the seed >> ")
        try:
            if (int(input) > 0):
                break
            else:
                print "You must enter a number greater than 0"
        except:
            print "You must enter a number greater than 0"
    maxHops = int(input[:])

    print 50*"#"
    print "seedURL: \t"+seedURL+"\nmaxFrontiers: \t"+str(maxFrontiers)+"\nmaxHops: \t"+str(maxHops)
    print 50*"#"

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

    print 50*"#"

    input = raw_input("Press enter to exit")
"""
if __name__ == "__main__":
    main()
"""
