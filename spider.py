import sys
import requests
import urlparse
import re
import queue
import settings
from robotparser import RobotFileParser
from BeautifulSoup import BeautifulSoup
from time import sleep
from copy import deepcopy
from database import DatabaseConnection
from stopwords import STOP_WORDS

urls_to_be_scraped = []
scraped_urls = []
black_list = []
inverted_index = {}

class Webpage(object):
    """
    Objects that refer to individual webpages. If the url is scrapeable the
    object will be filled with that data, indexed, and inserted into a database
    to be searched.
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
        if self.url not in urls_to_be_scraped and self.url not in black_list:
            self.need_to_be_scanned = True
        else:
            self.need_to_be_scanned = False

    def page_robot_scannable(self):
        """
        Checks whether the page is allowed to be crawled
        """
        if self.need_to_be_scanned is True:
            # REFACTOR to remove try statement.
            try:
                headers = {'User-agent':settings.SPIDER_USER_AGENT}
                self.urlparse = urlparse.urlparse(self.url)
                self.robotcheck = RobotFileParser()
                self.robotcheck.set_url('http://'+self.urlparse[1]+'/robots.txt') # Only works with http right now.
                self.robotcheck.read()
                self.need_to_be_scanned = self.robotcheck.can_fetch(settings.SPIDER_USER_AGENT, self.url)
            except:
                self.need_to_be_scanned = False

    def get_page(self):
        """
        The url is requested with a GET request. The page html is scraped
        directly, while elements of it aee scraped in parse_page
        """
        self.headers = {'User-agent':settings.SPIDER_USER_AGENT}
        #REFACTOR to remove try
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
        #REFACTOR to remove try from the logic
        try:
            pagerank[item]['number of outgoing links'] = len(dictionary_of_outgoing_links[item])
        except KeyError: #If a page was linked to but it was not scanned there will be a KeyError. This will fill in the "best known" information for that record.
            pagerank[item] = {'number of outgoing links': 0, 'incoming links':[]}
            for subitem in pagerank:
                #REFACTOR to remove try
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
            pagerank[item]['pagerank'] = (1-settings.PAGERANK_DAMPING)+subeqn*(settings.PAGERANK_DAMPING)
    pagerankprev = {}
    for item in pagerank:
        pagerankprev[item] = pagerank[item]['pagerank']
    return pagerankprev

def main(seed_url=None, max_pages=settings.DEFAULT_MAX_PAGES):
    """
    Instantiate the provided seed and start scraping starting at its url. Stop
    scraping when max pages has been hit.
    """
    if(seed_url is not None):
        urls_to_be_scraped.append(seed_url)
        for url in urls_to_be_scraped:
            if Webpage.instanceID > maxpages:
                break
            url = Webpage()
            url.load_url(url=seed_url)
            url.page_robot_scannable()
            if url.need_to_be_scanned is True:
                url.get_page()
                url.parse_parge()
                url.inverted_index_page()
                url.set_page_scanned()
            else:
                url.set_page_scanned()
            sleep(settings.REQUEST_TIME_INCREMENT)

        #Eventually look into a matrix math library for pagerank calculations
        dictionary_of_outgoing_links = {}
        for item in scraped_urls:
            if item.pagehtml:
                dictionary_of_outgoing_links[item.url] = item.pagelinks
        page_rank_dictionary = page_rank(outgoing_links_to_pagerank(dictionary_of_outgoing_links), settings.PAGERANK_ITERATIONS)

        dbconnection = DatabaseConnection()
        dbconnection.connect()
        for item in scraped_urls:
            if item.pagehtml:
                to_insert = {'title':item.title,
                             'url':item.url,
                             'pagehtml':item.pagehtml,
                             'pagetext':item.pagetext,
                             'pagerank':page_rank_dictionary[item.url],
                             'date':datetime.datetime.now()}
                dbconnection.load_document(to_insert)
                dbconnection.insert_document(scrape_data)

        for word in inverted_index:
            to_insert = {'word':word,
                         'date':datetime.date.today(),
                         'offsets':'BLAH'}
            dbconnection.load_document(to_insert)
            dbconnection.insert_document('inverted_index')
