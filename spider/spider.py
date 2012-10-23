import requests
import BeautifulSoup
#import time
import urlparse
from google.appengine.ext import db
import itertools
import re
import robotparser

URLList, linkCache, blacklist = [], {}, []

#testing
whitelist = ['127.0.0.1']

class scrapeData(db.Model): #db schema
    title = db.StringProperty()
    text = db.TextProperty()
    scrapeData = db.DateTimeProperty(auto_now_add=True)
    parent = db.StringProperty()
    rank = db.IntegerProperty()

class URL():
    _instanceID = itertools.count(0)

    def __init__(self, URL):
        self.URL = URL
        self.count = self._instanceID.next()

    def getPage(self):
        headers = {'User-agent':'Toastie'}
        #check robots. If robots says no scanning, throw out page
        #robotcheck = requests.get(urlparse.urlparse(URL)[1]+/robots.txt')

        #testing
        if urlparse.urlparse(self.URL)[1] in whitelist:
            self.request = requests.get(URL, headers=headers)
            self.soup = BeautifulSoup.BeautifulSoup(self.request.text)
        else:
            self.error = True

    def visibleElements(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return False
        elif re.match('<!--.*-->', str(element)):
            return False
        return True

    def parsePage(self):
        self.title = self.soup.find('title').text
        self.text = self.soup.findAll(text=true)
        self.pageText = ''

        for item in filter(visibleElements, self.text):
            if item != '\n':
                visibleText = visibleText+item
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
                if link in linkCache[self.URL]:
                    pass
                else:
                    linkCache[self.URL].append(link)
            else:
                URLList.append(link)
                linkCache[self.URL]=[link]

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

    def URLProcess(input):
        input.getPage()
        if "error" not in dir(input):
            input.parsePage()
        #time.sleep(1)
        #Consider pulling time interval from robots.txt
        print "hop="+str(input.hop), "instance="+str(input), "len(URLDir)="+str(len(URLDir)), "URL="+input.URL

    for index, item in enumerate(URLDir):
        if urlparse.urlparse(item.URL)[1] != "buttbox:8002":   #local testing
            continue
        if (index > maxFrontiers):
            break
        if (item.hop > maxHops):
            break
        print "Page "+str(index),
        URLProcess(item)

    print 50*"#"

    input = raw_input("Press enter to exit")

if __name__ == "__main__":
    main()


"""
database schema:
    table: websites
    url:    varchar(255)
    inside_hitcounts: int(16)
    outside_hitcounts: int(16)
    rank: int(2)
    title:  varchar(255)
    meta:   varchar(1024)
    page:   varchar(65536)
    date:   datetime
"""
